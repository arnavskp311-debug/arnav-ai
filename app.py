import os
from http.server import BaseHTTPRequestHandler

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(CURR_DIR, "index.html")

def get_html_bytes():
    try:
        with open(INDEX_FILE, "rb") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading index.html: {e}</h1>".encode("utf-8")

# Vercel BaseHTTPRequestHandler entrypoint
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = get_html_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_HEAD(self):
        content = get_html_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()

# Vercel WSGI entrypoint
def app(environ, start_response):
    content = get_html_bytes()
    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(content)))
    ])
    return [content]

# Aliases for all standard Python serverless conventions
application = app
Handler = handler
