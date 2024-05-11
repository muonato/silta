#!/usr/bin/env python3
# github/muonato/silta
# www.gnu.org/licenses

"""Silta utility functions and constants.

"""
import time
import json
import base64

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
        folder -- JSON file without suffix

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

def timestamp():
    """Returns localtime formatted.

    """
    return time.strftime("%d.%m.%Y %H:%M", time.localtime())

def decode_icon(params):
    """Encodes picture in folder 'ui/icons/' to base64 text.

    Args:
        params -- List of dictionaries with filename as value to 'task_icon' key

    Returns:
        params array with dictionaries 'task_icon' file encoded as base64

    """
    for data in params:
        if "task_icon" in data:
            if data["task_icon"]:
                try:
                    with open(f"ui/icons/{data['task_icon']}", "rb") as icon:
                        img = base64.b64encode(icon.read()).decode("utf-8")
                        data.update({"task_icon":f"data:image/png;base64,{img}"})
                except Exception:
                    err_message(f"Unable to decode \"ui/icons/{data['task_icon']}\"")
                    data.update({"task_icon":""})
                    pass

    return params

LOGIC_F = load_json("data/logic.json")
TEMPLATE_KEYS = ["BODY", "TASK", "TEXT", "NOTE", "SUMM", "LINK", "HREF", "ICON", "NONE"]
