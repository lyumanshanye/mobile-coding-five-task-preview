"""Offline mail test service. Never connects to SMTP/IMAP."""
import argparse
import hashlib
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=8765)
parser.add_argument("--db", default="mock-mail.sqlite3")
args = parser.parse_args()
db = sqlite3.connect(args.db)
db.execute("CREATE TABLE IF NOT EXISTS accepted(account_id TEXT, request_id TEXT, digest TEXT, response TEXT, PRIMARY KEY(account_id,request_id))")
db.execute("CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT)")
db.execute("INSERT OR IGNORE INTO settings VALUES('mode','normal')")
db.commit()

class Handler(BaseHTTPRequestHandler):
    def respond(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path != "/state":
            return self.respond(404, {})
        rows = db.execute("SELECT account_id,request_id,digest,response FROM accepted").fetchall()
        self.respond(200, {"mode": db.execute("SELECT value FROM settings WHERE key='mode'").fetchone()[0],
                          "accepted": [dict(zip(["account_id","request_id","digest","response"], r)) for r in rows]})

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 10485760:
                return self.respond(400, {"error":"invalid body length"})
            body = json.loads(self.rfile.read(size))
            if self.path == "/reset":
                db.execute("DELETE FROM accepted")
                db.execute("UPDATE settings SET value='normal' WHERE key='mode'")
                db.commit()
                return self.respond(200, {"reset":True})
            if self.path == "/mode":
                mode = body["mode"]
                if mode not in ("normal","offline","accept_then_timeout"):
                    return self.respond(400, {"error":"invalid mode"})
                db.execute("UPDATE settings SET value=? WHERE key='mode'", (mode,))
                db.commit()
                return self.respond(200, {"mode":mode})
            if self.path != "/send":
                return self.respond(404,{})
            account, request, payload = body["account_id"], body["request_id"], body["payload"]
            if account not in ("work","personal") or not isinstance(request,str) or not request or not isinstance(payload,dict):
                return self.respond(400, {"error":"invalid request"})
            digest = hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
            mode = db.execute("SELECT value FROM settings WHERE key='mode'").fetchone()[0]
            if mode == "offline":
                return self.respond(503, {"error":"offline"})
            old = db.execute("SELECT digest,response FROM accepted WHERE account_id=? AND request_id=?", (account,request)).fetchone()
            if old:
                return self.respond(200,json.loads(old[1])) if old[0] == digest else self.respond(409,{"error":"idempotency conflict"})
            result = {"server_id":account+":"+request,"accepted":True}
            db.execute("INSERT INTO accepted VALUES(?,?,?,?)",(account,request,digest,json.dumps(result)))
            db.commit()
            if mode == "accept_then_timeout":
                # Deliberately lose the response after durable acceptance.
                self.close_connection = True
                self.connection.shutdown(2)
                self.connection.close()
                return
            self.respond(200,result)
        except (KeyError,ValueError,TypeError):
            self.respond(400,{"error":"invalid JSON request"})

HTTPServer((args.host,args.port), Handler).serve_forever()

