#!/usr/bin/env python3
# github/muonato/silta
# www.gnu.org/licenses

"""Silta main logic library.

Exports class Silta() as facade to application.

Usage:
  silta = Silta("data/silta.db", "ui/silta")

"""
from urllib.parse import parse_qsl

from silta.sqlte import SQLiteDB
from silta.webui import Frontend

import silta.utils as util

class Silta:
    """Bridge between database and user interface.

    Args:
        sqlt_file -- Path to sqlite database file
        theme_dir -- Directory for HTML templates

    Usage:
        silta = Silta('<db-file>', 'ui-directory')

    """
    def __init__(self, sqlt_file, theme_dir):

        # store database handler
        self.db = SQLiteDB(sqlt_file)
        
        # store ui handler
        self.ui = Frontend(
            theme_dir, util.htm_data(theme_dir))

        # read usecase configs
        self.uc = util.LOGIC_F

    def get_qsl(self, shttp_qsl, auth_head=None):
        """Parse URL query string.

        Args:
            shttp_qsl -- Web browser URL query string.
            auth_head -- HTTP authorization header.

        Returns:
            Web page to instance variable self.html

        """
        # store usecase f-strings
        self.fs = {"db":self.db.name}

        try:
            # convert query string to dictionary
            qs_dict = dict(parse_qsl(shttp_qsl)) \
                        if shttp_qsl else {"uc":"1"}

            # store all but empty qsl values to f-string dict
            self.fs.update({k: v for k, v in qs_dict.items() \
                            if not v == 'none'})

            # get current use-case index number
            self.ix = int(qs_dict.get("uc", 1))

            # update UI html
            self.put_fstr()

        except Exception as err:
            self.ui.html_update(
                util.err_message(f"{err}"))

        # finalize result page
        self.ui.html_public()

        return self.ui.html

    def add_template(self, task_chain):
        """Duplicates template task chain to merge into task.

        Args:
            task_chain -- Array of table rows as dictionaries.

        """
        last_id = self.db.runsql(
            "SELECT seq FROM SQLITE_SEQUENCE WHERE name='tasks';")[0]["seq"]

        next_id = last_id + 1

        self.db.runsql(
            "CREATE TEMP TABLE tmp_tasks (task_id, task_host, task_done, task_name);")

        self.db.runsql(
            "CREATE TEMP TABLE tmp_attrs (attr_id, attr_host, attr_type, attr_name, attr_data);")

        attr_chain = self.db.runsql(
            f"WITH RECURSIVE attr_chain(n) AS (VALUES({self.fs['ti']}) \
                UNION SELECT attr_id FROM attrs, attr_chain \
                WHERE attrs.attr_host=attr_chain.n) \
                SELECT * FROM attrs WHERE attr_id IN attr_chain;")

        for data in task_chain:
            for attr in attr_chain:
                if attr["attr_host"] == data["task_id"]:
                    attr.update({"attr_host":next_id})

                    if attr["attr_type"] != "TMPL":
                        if attr["attr_type"] == "TIME":
                            attr.update({"attr_data":util.timestamp()})

                        self.db.runsql(
                            f"INSERT INTO tmp_attrs (attr_id, attr_host, attr_type, attr_name, attr_data) \
                                VALUES ({attr['attr_id']}, {attr['attr_host']}, \
                                    \"{attr['attr_type']}\", \"{attr['attr_name']}\", \"{attr['attr_data']}\");")
# TESTING ONLY
                        print(f"\033[1;33mattr data:\033[0m {attr}")
#                        print(f"\033[1;33mDTA {template}:\033[0m {sql_data}")

            for host in task_chain:            
                if host["task_host"] == data["task_id"]:
                    host.update({"task_host":next_id})

            # convert python None to sqlt
            if data["task_host"] == None:
                if "th" in self.fs:
                    data.update({"task_host":self.fs["th"]})
                else:
                    data.update({"task_host":"NULL"})

            data.update({"task_id":next_id})

            self.db.runsql(
                f"INSERT INTO tmp_tasks (task_id, task_host, task_done, task_name) \
                    VALUES ({data['task_id']}, {data['task_host']}, 0, \"{data['task_name']}\");")
 
            next_id = next_id + 1

        self.db.runsql("UPDATE tmp_tasks SET task_id = NULL;")
        self.db.runsql("UPDATE tmp_attrs SET attr_id = NULL;")

        self.db.runsql("INSERT INTO tasks SELECT * FROM tmp_tasks;")
        self.db.runsql("INSERT INTO attrs SELECT * FROM tmp_attrs;")

        self.db.runsql("DROP TABLE tmp_tasks;")
        self.db.runsql("DROP TABLE tmp_attrs;")

    def put_fstr(self):
        """Update f-strings on user interface

        """
        queue = self.ix

        # update unoccupied
#        self.ui.html_update(
#            self.uc[0]['F-STRINGS'])

        # set defaults
#        self.fs.update(
#            self.uc[0]["F-STRINGS"])

        while queue:
            # usecase f-str
            self.fs.update(
                self.uc[queue]["F-STRINGS"])

# TESTING ONLY
            print(f"\033[1;31m{self.uc[queue]['METADATA']['description']}\033[0m\n\033[1;33mself.fs:\033[0m {self.fs}")
            # put body attributes
            self.ui.html_reload()
            self.ui.html_update(self.fs)

            # to template
            sql_data = []
            for template,sql in self.uc[queue]["TEMPLATES"].items():
                for cmd in sql:
                    sql_data = self.db.runsql(
                                    cmd.format(**self.fs))

# TESTING ONLY
                    print(f"\033[1;33mSQL {template}:\033[0m {cmd.format(**self.fs)}")
                    print(f"\033[1;33mDTA {template}:\033[0m {sql_data}")
                    self.ui.html_export(sql_data, template)

                    # export sql to body
                    for data in sql_data:
                        self.ui.html_update(data)

            # task template
            if queue == 16:
                self.add_template(sql_data)

            # status selector
            if "fw" in self.fs:
                self.fs.update(
                    {"ti":self.fs["th"]})

                queue = int(self.fs["fw"])
                del self.fs["fw"]
            else:
                queue = self.uc[queue]["METADATA"]["daisy-chain"]
                if queue:
                    for data in sql_data:
                        self.fs.update(data)

            # update unoccupied
            self.ui.html_update(
                self.uc[0]['F-STRINGS'])

