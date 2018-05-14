from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl
import json

class QueryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        parsed_path = urlparse(self.path)
        print("Path", self.path)
        queries = dict(parse_qsl(parsed_path.query))
        print(queries)
        self.wfile.write(json.dumps({'q':queries['q']}).encode())
        return


if __name__ == '__main__':
    address, port = '0.0.0.0', 4000
    server = HTTPServer((address, port), QueryHandler)
    try:
        print("Server was started on {}:{}".format(address, port))
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server shut down")
