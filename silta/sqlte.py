#!/usr/bin/env python3
# github/muonato/silta
# www.gnu.org/licenses

"""Silta SQLite database routines.

Exports class Silta() as facade to application.

Usage:
    database = SQLiteDB('/path/to/dbase')

"""
import sqlite3

class SQLiteDB:
    """Handle sqlite3 database connection.

    Args:
        f -- Database filename

    """
    def __init__(self, f):
        self.name = f
        self.conn = sqlite3.connect(f)

        # create new database from default schema if missing
        if self.runsql("SELECT * FROM sqlite_master") == []:
            with open("data/silta.db.sql") as create_db:
                self.runsql(create_db.read())

    def __del__(self):
        self.conn.close()

    def dicto(self, dict_arr):
        """Merge list of dictionaries with string values only.

        Args:
            dict_arr: List of dictionaries

        Returns:
            Single dictionary with strings of same key joined.
        """
        merged = {}
        for dictionary in dict_arr:
            for key, val in dictionary.items():
                merged[key] = "\n".join([merged[key], val]) \
                                    if key in merged else val
        return merged

    def runsql(self, sql_cmd, to_dict=False):
        """Run SQL statement on database.

        Args:
            sql_cmd: String statement to commit.
            to_dict: Return results as single dictionary.

        Returns:
            Results as list of dictionaries, dict lambda by 
            https://stackoverflow.com/users/3419103/falko

        """
        try:
            self.conn.row_factory = lambda C, R: {
                c[0]: R[i] for i, c in enumerate(C.description)
            }
            c = self.conn.cursor()
            if sql_cmd.startswith("BEGIN"):
                c.executescript(sql_cmd)
            else:
                c.execute(sql_cmd, ())

            self.conn.commit()
            fetch = c.fetchall()

            return self.dicto(fetch) if to_dict else fetch

        except BaseException as err:
            print(f"dbase.py {err=}")

            return []
