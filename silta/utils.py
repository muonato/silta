#!/usr/bin/env python3
# github/muonato/silta
# www.gnu.org/licenses

"""Silta utility functions and constants.

"""
import time
import json

def load_json(json_file):
    """Reads JSON formatted text file.

    Args:
        json_file -- filename to read
    """
    try:
        with open(json_file) as f:
            fstr = json.load(f)

    except FileNotFoundError:
        fstr = []

    return fstr


def htm_data(folder):
    """Reads user interface templates file.

    Args:
        folder -- Path to JSON file (without suffix)

    """
    return load_json(f"{folder}.json")

def err_message(errstr):
    """Prints error message from exception.

    Args:
        errstr -- error string (err=)

    """
    print("\033[1;31mException\033[0m - - {} {}".format(
        time.strftime("[%d/%b/%Y %H:%M:%S]", time.localtime()), errstr))

    # UI template
    message = {
        "note-css":"fail",
        "show-notify":"block",
        "show-toolbar":"none",
        "show-task":"none",
        "note-msg":errstr,
        "TASK":""
    }

    return message

LOGIC_F = load_json("data/logic.json")
TEMPLATE_KEYS = ["BODY", "TASK", "TEXT", "NOTE", "NONE"]
