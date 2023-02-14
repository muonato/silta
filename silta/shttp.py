#!/usr/bin/env python3
#
# SIMPLE LOCALIZED TASKS
# Copyright 2022 muonato
#   GNU License GPL v3

import http.server

from os import path
from urllib import parse

class Handler(http.server.SimpleHTTPRequestHandler):
    """Customized http server request and response handling"""

    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

    def do_AUTH(self):
        """Sends authorization request header to web browser"""

        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"SILTA\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Sends query string to parser and prints response"""

        authz = self.headers.get('Authorization')
        if -1 < self.path.find("uc=0") and authz == None:
            self.do_AUTH()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
 
        query = parse.urlparse(self.path).query
        whtml = self.silta.get_msg(query, authz)

        self.wfile.write(bytes(whtml, "utf-8"))
