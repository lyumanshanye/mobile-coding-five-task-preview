"""Local deterministic discovery/media fixture; no external services or proxy."""
import argparse
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import re
import time
from urllib.parse import urlparse,parse_qs

ROOT=Path(__file__).resolve().parent
CATALOG=json.loads((ROOT/'catalog.json').read_text())


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url=urlparse(self.path);query=parse_qs(url.query)
        if url.path=='/search':
            q=query.get('q',[''])[0];page=int(query.get('page',['1'])[0])
            time.sleep(1.2 if q=='slow' else .05)
            rows=CATALOG['items']
            found=[rows[0]] if q=='slow' else rows[:2] if page==1 else [rows[1],rows[2]]
            payload=json.dumps(dict(query=q,page=page,items=found,next_page=2 if page==1 and q!='slow' else None)).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload);return
        if url.path.startswith('/media/'):
            name=url.path.removeprefix('/media/')
            if not re.fullmatch(r'[a-z0-9_-]+\.mp4',name):self.send_error(404);return
            path=ROOT/'media'/name
            if not path.is_file():self.send_error(404);return
            content=path.read_bytes();start,end=0,len(content)-1;partial=False
            requested=self.headers.get('Range')
            if requested:
                match=re.fullmatch(r'bytes=(\d+)-(\d*)',requested)
                if not match:self.send_error(416);return
                start=int(match.group(1));end=min(int(match.group(2)) if match.group(2) else end,end);partial=True
                if start>end:self.send_error(416);return
            self.send_response(206 if partial else 200);self.send_header('Content-Type','video/mp4');self.send_header('Accept-Ranges','bytes')
            self.send_header('Content-Length',str(end-start+1))
            if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{len(content)}')
            self.end_headers();self.wfile.write(content[start:end+1]);return
        self.send_error(404)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8765);args=p.parse_args()
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
