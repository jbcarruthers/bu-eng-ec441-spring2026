"""EC 441 L23 -- trivial HTTP server using Python's standard library.

The point of this demo: everything HTTP/1.1 is doing is buildable on top of
the socket API from L22. Python's http.server is about 500 lines of code
sitting on a TCP listen socket.

Run:
    python3 demo_http_server_l23.py
Then in another shell:
    curl -v http://127.0.0.1:8080/
    curl -v http://127.0.0.1:8080/index.html

Or serve the current directory with the stdlib one-liner (no script needed):
    python3 -m http.server 8080

Stop with Ctrl-C.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone

PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (
            "<!DOCTYPE html>\n"
            "<html><head><title>EC 441 L23</title></head>\n"
            "<body>\n"
            f"  <h1>Hello from a Python HTTP server</h1>\n"
            f"  <p>Path: <code>{self.path}</code></p>\n"
            f"  <p>Time: {datetime.now(timezone.utc).isoformat()}</p>\n"
            f"  <p>Client: {self.client_address[0]}:{self.client_address[1]}</p>\n"
            "</body></html>\n"
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Course", "EC441")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")


def main():
    srv = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"HTTP/1.1 server on http://127.0.0.1:{PORT}/  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
