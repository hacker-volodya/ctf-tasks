#!/usr/bin/env python3
import http.server, ssl

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Flag is HV{f448f1151ae4a28131a414f1f67cb0ec}")
        self.wfile.close()

server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, MyHandler)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.set_ciphers("AES256-GCM-SHA384")
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()