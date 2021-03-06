#!/usr/bin/env python2
# coding: utf8

from __future__ import print_function

import sys
from SocketServer import ForkingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from .config import RioConfig
from .streamer import icystream
from .utilities import render_headers


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # FIXME: When the content-type changes between streams, we're probably
        # boned.
        config = RioConfig()
        self.headers['client'] = "{}:{}".format(*self.client_address)
        pretty_headers = render_headers(self.headers.dict)
        msg = u"Client Connected:\n{}".format(pretty_headers)
        msg = msg.replace('\n', '\n\t')
        print(msg, file=sys.stderr)
        config.forward_metadata = 'icy-metadata' in self.headers
        self.send_response(200)
        self.send_header('Content-type', 'audio/mpeg')
        if config.forward_metadata:
            self.send_header('icy-metaint', str(config.ICY_METAINT))
        self.end_headers()
        try:
            for stream in config.cycle_streams():
                icystream(stream, self.wfile, config=config)
        except KeyboardInterrupt:
            pass


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    pass


def serve_on_port(host, port):
    server = HTTPServer((host, port), Handler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
