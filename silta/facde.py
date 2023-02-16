#!/usr/bin/env python3
#
# SIMPLE LOCALIZED TASKS
# Copyright 2022 muonato
#   GNU License GPL v3

from silta.sqlte import DB_SQLite
from silta.webui import Frontend

from silta.utils import load_attr
from urllib.parse import parse_qsl

class Silta:
    """Interconnect user interface and database.

    Args:
        sqlt_file: Path to sqlite database file
        theme_dir: Directory for HTML templates

    Usage:
        silta = Silta('data/silta.db', 'ui/default')
    """
    def __init__(self, sqlt_file, theme_dir, mysql_db):
        self.db = DB_SQLite(sqlt_file)
        self.ui = Frontend(theme_dir)

        if mysql_db:
            try:
                from silta.mysql import DB_MySQL
                self.mysql = DBMySQL(mysql_db)
            except ImportError:
                self.mysql = None

        # use case SQL commands and attributes for UI
        self.uc = load_attr(f"{theme_dir}/lang.json")
        self.HTM_COMMON_FS = self.uc[0]["HTM_COMMON"]

    def get_msg(self, shttp_qsl, auth_head=None):
        """Parse URL query string to process use case.

        Args:
            shttp_qsl: Web browser URL query string.
            auth_head: HTTP authorization header.

        Returns:
            Web page to instance variable self.html
        """
#        try:
        if True:
            if shttp_qsl == "":
                shttp_qsl = "uc=1"

            qs_dict = dict(parse_qsl(shttp_qsl))
            self.ix = int(qs_dict.get("uc", 1))
            self.fs = {k: v for k, v in qs_dict.items() \
                            if not v == 'none'}
            self.state_m()
#        except BaseException as err:
        else:
            self.ui.note(f"facde.py {err=}\n", "warn")

        self.ui.build()

        return self.ui.html

    def sql_list(self, idx, key):
        """Run a list of consecutive SQL statements.

        Args:
            idx: Index in the use case definitions list.
            key: Dictionary key to list of SQL clauses.

        Returns:
             Single dictionary with results from each query.
        """
        fstr = {}
        for sql_cmd in self.uc[idx]["SQL_CLAUSE"][key]:
            fstr.update(
                self.db.runsql(
                    sql_cmd.format(**self.fs), to_dict=True))
        
        return fstr

    def sql_tags(self, idx, key):
        """Run SQL statements tagged with dictionary key.

        Args:
            idx: Index in the list of dictionaries.
            key: Dictionary key of SQL clause, tuple for joins.

        Returns:
            List of database result columns as dictionaries.
        """
        if isinstance(key, tuple):
            sql_cmd = ""
            for tag in key:
                sql_cmd = " ".join(
                    [sql_cmd, self.uc[idx]["SQL_CLAUSE"][tag]])
        else:
            sql_cmd = self.uc[idx]["SQL_CLAUSE"][key]

        return self.db.runsql(
                    sql_cmd.format(**self.fs))

    def submit(self):
        """Update database table row with data submitted on HTML form."""

        if self.fs["ok"] == "DEL":
            self.sql_tags(self.ix, "DELETE_ROW")

        elif "sp" in self.fs:
            self.sql_tags(self.ix, "SPECIAL_FN")           

        elif self.fs["id"] == "0":
            self.sql_tags(self.ix, "INSERT_ROW")
            last_row = self.db.runsql("SELECT last_insert_rowid() AS id").pop()
            self.fs = {**self.fs, **last_row}
        else:
            curr_row = self.sql_tags(self.ix, "SELECT_RAW").pop()
            self.fs = {**curr_row, **self.fs}
            self.sql_tags(self.ix, "UPDATE_ROW")

        self.ix = self.uc[self.ix]["HTM_OBJECT"]["HOST_UC"]
        self.fs = {
            "uc": self.ix,
            "id": self.fs.get("hi", None)}
         
    def state_m(self):
        """Query the database and set f-strings on html template"""

        self.fs.update(self.HTM_COMMON_FS)

        if "ok" in self.fs:
            self.submit()

        if self.fs.get("id", None) is None:
            self.fs.update(
                self.uc[self.ix]["HTM_NAVDIV"])
            self.ui.page_append(
                    self.sql_tags(
                            self.ix, ("SELECT_ROW","BY_KEYWORD") \
                            if "fk" in self.fs else ("SELECT_ROW","SORT_ORDER")))
        else:
            self.fs.update(
                        self.uc[self.ix]["HTM_OBJECT"])
            self.fs.update(
                        self.sql_list(self.ix, "SELECT_OPT"))
            self.fs.update(
                        self.sql_tags(
                            self.ix, ("SELECT_ROW", "BY_ROW_IDX")).pop())

            if "LINK_UC" in self.uc[self.ix]["HTM_OBJECT"]:
                self.ui.page_append(
                        self.sql_tags(
                                self.uc[self.ix]["HTM_OBJECT"]["LINK_UC"],
                                ("SELECT_ROW", "BY_HOST_ID")))

        self.ui.page_update(self.fs)
