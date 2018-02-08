from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from build_html import build_html
from eve_loader import EveLoader
import SocketServer

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        # page input parsing and sanitizing
        i = self.path.find("page=")
        try:
            page = int(self.path[i+5:]) if i != -1 else 0
        except:
            page = 0

        eve.reload()
        html = build_html(eve.get_n_lines(100, page), page)
        self.wfile.write(html)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        # content_length = int(self.headers['Content-Length'])
        # post_data = self.rfile.read(content_length)
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv, exit

    try:
        assert ( len(argv) in (2, 3) )
        port = int(argv[2]) if len(argv) == 3 else 80
    except:
        print "USAGE: python webserver.py /path/to/eve.json [port=80]"
        exit(1)

    global eve
    eve = EveLoader(argv[1])

    run(port=port)
