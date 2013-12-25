#!/usr/bin/env python2
# coding: utf8

from __future__ import print_function

import sys
import itertools
from SocketServer import ForkingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from requests import ConnectionError

from .config import HOST, PORT, STREAMS, ICY_METAINT
from .streamer import icystream
from .utilities import render_headers


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # FIXME: When the content-type changes between streams, we're probably
        # boned.
        print("\n{}\n".format(render_headers(self.headers)), file=sys.stderr)
        forward = 'icy-metadata' in self.headers
        self.send_response(200)
        self.send_header('Content-type', 'audio/mpeg')
        if forward:
            self.send_header('icy-metaint', str(ICY_METAINT))
        self.end_headers()
        try:
            for url in itertools.cycle(STREAMS):
                icystream(url, self.wfile, forward_metadata=forward)
        except ConnectionError as e:
            print(e)
        except KeyboardInterrupt:
            pass


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    pass


def serve_on_port(host=HOST, port=PORT):
    server = HTTPServer(("localhost", port), Handler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
