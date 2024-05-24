#!/usr/bin/env python3
# github/muonato/silta

"""Silta application launcher.

Args:
    -a --address
    -p --port
    -d --database
    -t --theme
    -h --help
"""
import argparse
import socketserver

from silta.logic import Silta
from silta.shttp import Handler

def main():
    print(f"\n\t\tSILTA v1.0 Copyright 2022 -muonato-"\
            "\nReleased under the terms of "\
            "the GNU General Public License GPLv3\n")

    options = argparse.ArgumentParser(
                prog='app.py',
                usage='%(prog)s [options]',
                description="Simple Localized Tasks")

    options.add_argument("-a","--address", default="127.0.0.1",
                    help="server ip address, default: 127.0.0.1")
    options.add_argument("-p", "--port", default=8000,
                    help="server HTTP service port, default: 8000")
    options.add_argument("-d", "--database", default="data/silta.db",
                    help="sqlite database file")
    options.add_argument("-t", "--theme", default="suomi",
                    help="frontend theme name, default: 'suomi'")

    args = options.parse_args()

    Handler.silta = Silta(args.database, args.theme)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(
            (args.address, int(args.port)), Handler) as httpd:
                try:
                    print(f"Socketserver {args.address}:{args.port} ")
                    httpd.serve_forever()

                except KeyboardInterrupt:
                    print("\nSocketserver shutdown.")
                    httpd.shutdown()
                    httpd.socket.close()

if __name__ == "__main__":
        main()
