#!/usr/bin/env python3
#
# SIMPLE LOCALIZED TASKS
# Copyright 2022 muonato
#   GNU License GPL v3

import json

ATTR_FILE = "data/silta.json"

def load_attr(lang_file):
    try:
        with open(lang_file) as f:
            lang = json.load(f)
            
    except FileNotFoundError:
        lang = []

    with open(ATTR_FILE) as f:
        attr = json.load(f)

    for i, d in enumerate(lang):
        for key in ["HTM_COMMON", "HTM_OBJECT", "HTM_NAVDIV"]:
            if key in d:
                attr[i][key].update(d[key])
    return attr
