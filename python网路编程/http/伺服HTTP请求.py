#!/usr/bin/env python

import argparse
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # send message to browser
        self.wfile.write('Hello from server!')

class CustomHttpServer(HTTPServer):
    def __init__(self, host, port):
        server_address = (host, port)
        HTTPServer.__init__(self, server_address, RequestHandler)

def run_server(port):
    try:
        server = CustomHttpServer(DEFAULT_HOST, port)
        server.serve_forever()
    except Exception, err:
        print err
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Http Client Example')
    parser.add_argument('--port', action='store', dest='port', type=int ,default=DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    run_server(port)