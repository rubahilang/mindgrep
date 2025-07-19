from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from server_example")

def run():
    srv = HTTPServer(("localhost", 8000), Handler)
    print("Serving on http://localhost:8000")
    srv.serve_forever()

if __name__ == "__main__":
    run()
