#!/usr/bin/env python3
# github/muonato/silta
# www.gnu.org/licenses

"""Silta customized Simple HTTP Request Handler

"""
import http.server

from os import path
from urllib import parse

class Handler(http.server.SimpleHTTPRequestHandler):
    """Customized http server request and response handling

    """
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

    def do_GET(self):
        """Sends query string to parser and prints response

        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
 
        query = parse.urlparse(self.path).query
        whtml = self.silta.get_qsl(query)

        self.wfile.write(bytes(whtml, "utf-8"))
