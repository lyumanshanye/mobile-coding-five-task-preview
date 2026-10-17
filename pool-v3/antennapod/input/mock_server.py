"""Local deterministic RSS/audio fixture. Restart resets the one-shot failure."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parent/'server'
os.chdir(ROOT)
class Handler(SimpleHTTPRequestHandler):
    failed=False
    def do_GET(self):
        if self.path=='/episode3.wav' and not Handler.failed:
            Handler.failed=True
            self.send_error(503,'Deterministic first-attempt failure')
            return
        if self.path=='/feed.xml':
            data=(ROOT/'feed.xml').read_text().replace('FIXTURE_HOST',self.headers.get('Host','127.0.0.1:8765')).encode()
            self.send_response(200);self.send_header('Content-Type','application/rss+xml');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
            return
        super().do_GET()
ThreadingHTTPServer(('0.0.0.0',8765),Handler).serve_forever()
