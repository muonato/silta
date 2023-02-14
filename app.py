#!/usr/bin/env python3
#
# SIMPLE LOCALIZED TASKS
# Copyright 2022 muonato
#   GNU License GPL v3

import argparse
import socketserver

from silta.facde import Silta
from silta.shttp import Handler

def main():
    print(f"\n\t\tSILTA v1.0 Copyright 2022 muonato"\
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
    options.add_argument("-t", "--theme", default="ui/default",
                    help="browser theme folder, default: 'ui/default'")
    options.add_argument("-m", "--mysql", default=None,
                    help="mysql db, example: 'user:pass@address:port:database'")

    args = options.parse_args()

    Handler.silta = Silta(args.database, args.theme, args.mysql)

    with socketserver.TCPServer(
            (args.address, int(args.port)), Handler) as httpd:
                httpd.serve_forever()

if __name__ == "__main__":
        main()
