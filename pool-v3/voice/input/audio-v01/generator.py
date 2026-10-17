"""Generate original spoken media locally and verify decodability, not app playback."""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        parser.error("Local FFmpeg and ffprobe are required")
    raw = args.manifest.read_bytes()
    manifest = json.loads(raw)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "manifest.json").write_bytes(raw)
    (args.out / "generator.py").write_bytes(Path(__file__).read_bytes())
    (args.out / "scripts").mkdir()
    (args.out / "library").mkdir()
    report = {"status": "RUNNING", "purpose": "media_fixture_not_playback_validation",
              "started_at": time.time(), "origin": manifest["origin"], "files": []}
    try:
        version = subprocess.run([ffmpeg, "-version"], capture_output=True, check=True, timeout=30)
        (args.out / "ffmpeg-version.txt").write_bytes(version.stdout)
        report["ffmpeg_sha256"] = hashlib.sha256(Path(ffmpeg).read_bytes()).hexdigest()
        for index, chapter in enumerate(manifest["chapters"]):
            relative = Path(chapter["path"])
            if relative.is_absolute() or ".." in relative.parts or relative.suffix != ".mp3":
                raise ValueError("Invalid relative media path")
            script_name = f"scripts/chapter-{index:03d}.txt"
            (args.out / script_name).write_text(chapter["text"] + "\n")
            output = Path("library") / relative
            (args.out / output).parent.mkdir(parents=True, exist_ok=True)
            command = [ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-n", "-f", "lavfi",
                       "-i", f"flite=textfile={script_name}:voice={manifest['voice']}",
                       "-ar", "24000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "64k",
                       "-metadata", "title=" + chapter["title"], "-metadata", "album=" + chapter["book"],
                       "-metadata", "track=" + str(chapter["track"]), str(output)]
            generated = subprocess.run(command, cwd=args.out, capture_output=True, timeout=180)
            (args.out / f"generate-{index:03d}.log").write_bytes(generated.stdout + generated.stderr)
            if generated.returncode:
                raise RuntimeError(f"Synthesis failed for {relative}")
            metadata = subprocess.run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(output)],
                                      cwd=args.out, capture_output=True, check=True, timeout=30)
            (args.out / f"probe-{index:03d}.json").write_bytes(metadata.stdout)
            decoded = subprocess.run([ffmpeg, "-nostdin", "-v", "error", "-i", str(output),
                                      "-ar", "24000", "-ac", "1", "-f", "s16le", "-"], cwd=args.out,
                                     capture_output=True, check=True, timeout=60)
            samples = array("h")
            samples.frombytes(decoded.stdout)
            duration = len(samples) / 24000
            rms = math.sqrt(sum(x * x for x in samples) / max(1, len(samples)))
            if duration < 15 or rms < 10:
                raise RuntimeError("Media is too short or silent")
            report["files"].append({"path": str(output), "sha256": hashlib.sha256((args.out / output).read_bytes()).hexdigest(),
                                    "decoded_duration_seconds": duration, "pcm_rms": rms,
                                    "sample_rate": 24000, "channels": 1, "command": command})
        report["status"] = "MEDIA_GENERATED_AND_DECODED"
    except Exception as error:
        report["status"] = "MEDIA_GENERATION_FAILED"
        report["error"] = str(error)
    finally:
        report["finished_at"] = time.time()
        (args.out / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"status": report["status"], "files": len(report["files"]), "error": report.get("error")}, indent=2))
    return 0 if report["status"] == "MEDIA_GENERATED_AND_DECODED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
