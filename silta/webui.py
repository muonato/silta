#!/usr/bin/env python3
# github/muonato/silta
# www.gnu.org/licenses

"""Silta user interface library.

Usage:
    ui = Frontend(html, json)

"""
from string import Formatter

class NamespaceFormatter(Formatter):
    """Customized string formatter class

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
                return "".join(["{", f"{key}", "}"])
        else:
            Formatter.get_value(key, args, kwds)

class Frontend:
    """Silta user interface class for HTML output.

    Args:
        html_home -- Template filename without suffix
        html_json -- Template JSON file without suffix

    """
    def __init__(self, html_home, html_json):

        # declare formatter object var
        self.fmt = NamespaceFormatter()

        # html template dict data
        self.TEMPL = html_json[0]

        # read ui html body template file
        with open(f"{html_home}.html") as f:
            self.TEMPL["BODY"] = f.read()

    def html_public(self):
        """Adds header to finalize HTML output page.

        Args:
            none
        """
        self.html_update({"HEAD":self.TEMPL["HEAD"]})
 
    def html_reload(self):
        """Resets the output with default template.

        Args:
            none
        """
        self.html = self.TEMPL["BODY"]
       
    def html_update(self, params):
        """Updates the HTML template with f-strings.

        Args:
            params -- Dictionary with f-string values.

        """
        self.html = self.fmt.format(self.html, **params)
            
    def html_export(self, params, template):
        """Exports f-string dict list to HTML template.

        Args:
            params -- List of dictionaries with f-string values
            template -- Template dict key (same as f-string tag)

        Returns:
            Calls function html_update

        """
        if template == "NONE":
            return False

        htm = ""
        
        for item in params:
            if template == "BODY":
                self.html_update(item)
            else:
                tmp = self.TEMPL[template]
                htm = "".join(
                    [htm, self.fmt.format(tmp, **item)])

        self.html_update({template:htm})

        return True
