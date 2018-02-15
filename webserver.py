from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse   import urlparse, parse_qs
from build_html import build_html, build_table_packet
from eve_loader import EveLoader
from filter import Filter
import signal
import sys

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        # input parsing and sanitizing
        query_components = parse_qs(urlparse(self.path).query)
        try:
            page = int(query_components["page"][0])
        except:
            page = 0
        try:
            order = query_components["order"][0]
            assert ( order in ("timestamp_d", "timestamp_a", "severity_a", "severity_d") )
        except:
            order = "timestamp_d"
        f = Filter()
        try:
            f.set_source(query_components["filter_src"][0])
        except:
            f.set_source()
        try:
            f.set_destination(query_components["filter_dst"][0])
        except:
            f.set_destination()
        try:
            f.set_sid(query_components["filter_sid"][0])
        except:
            f.set_sid()
        try:
            f.set_protocol(query_components["filter_protocol"][0])
        except:
            f.set_protocol()

        eve.reload() # check if the logfile has been updated
        html = build_html(eve.get_n_lines(100, page, order, f), page, order, f)
        self.wfile.write(html)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) 
        post_data      = self.rfile.read(content_length)
        try:
            i = post_data.find("id=")
            idd = int(post_data[i+3:])
            assert ( idd>=0 and idd<=eve.max_db_index )
            payload, packet = eve.get_packet_by_id(idd)
            content = build_table_packet(payload, packet)
            self.wfile.write("<html><body> " + content + " </body></html>")
        except:
            self.wfile.write("<html><body> id error </body></html>")

def signal_handler(signal, frame):
    print "\nStopping httpd..."
    eve.quit()
    sys.exit(0)

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv, exit

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        assert ( len(argv) in (2, 3) )
        port = int(argv[2]) if len(argv) == 3 else 80
    except:
        print "USAGE: python webserver.py /path/to/eve.json [port=80]"
        exit(1)

    global eve
    eve = EveLoader(argv[1])
    run(port=port)
