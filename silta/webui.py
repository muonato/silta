#!/usr/bin/env python3
#
# SIMPLE LOCALIZED TASKS
# Copyright 2022 muonato
#   GNU License GPL v3

from string import Formatter

class NamespaceFormatter(Formatter):
    """String formatter class to handle undefined f-strings:
    https://peps.python.org/pep-3101/#customizing-formatters
    """

    def __init__(self, namespace={}):
        Formatter.__init__(self)
        self.namespace = namespace

    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                return "none"
        else:
            Formatter.get_value(key, args, kwds)

class Frontend:
    """Builds HTML page for the user interface.

    Args:
        html_home: Home directory for HTML templates.
    """

    def __init__(self, html_home):
        with open(f"{html_home}/head.html") as f:
            self.HEAD = f.read()

        with open(f"{html_home}/body.html") as f:
            self.BODY = f.read()

        with open(f"{html_home}/link.html") as f:
            self.LINK = f.read()

        self.FOOT = "\t\t</div>\n</body>\n</html>"
        self.page = self.BODY

    def note(self, msg, css="info"):
        """Display the notification section of page"""

        self.page_update(
                {"note-css":css, "note-show":"block", "note-msg":msg})

    def page_update(self, params):
        """Update the dynamic page section with f-strings.

        Args:
            params: Dictionary with f-string values.
        """
        fmt = NamespaceFormatter()
        self.page = fmt.format(self.page, **params)
            
    def page_append(self, params):
        """Append the linked items section to page content.

        Args:
            params: List of dictionaries with f-string values.
        """
        fmt = NamespaceFormatter()
        for item in params:
            self.page = "".join([self.page, fmt.format(self.LINK, **item)])
 
    def build(self):
        """Combine html sections and reset page content"""

        self.html = "".join([self.HEAD, self.page, self.FOOT])
        self.page = self.BODY
