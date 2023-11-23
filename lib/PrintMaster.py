#!/usr/bin/env python3
# coding : utf-8
# PrintMaster

import sys
import shutil
import unicodedata

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count = count + 1
    return count

class Printer:
    """ Printer Class """

    """
    config = {
        "name" : "NAME",
        "sub-name" : "SUB-NAME",
        "len" : 32,
        "screen-full" : True,
    }
    """

    def __init__(self):
        self.prefix = ""
        self.len = 65536
        self.screen_full = False

    def setConfig(self, config):
        self.prefix = ""
        self.name_string = ""
        self.sub_string = ""
        self.config = config
        if "name" in config.keys():
            if not config["name"] is None:
                self.name = config["name"]
                self.name_string = f"[{self.name}]"
            else:
                self.name = ""
                self.name_string = ""
        if "sub-name" in config.keys():
            if not config["sub-name"] is None:
                self.sub_name = config["sub-name"]
                self.sub_string = f"[{self.sub_name}]"
            else:
                self.sub_name = ""
                self.sub_string = ""
        if "len" in config.keys():
            self.len = config["len"]
        if "screen-full" in config.keys():
            self.screen_full = config["screen-full"]
        self.prefix = f"{self.name_string}{self.sub_string}"

    def print(self, string, end = "\r\n", file = sys.stdout):
        if self.screen_full:
            term_size = shutil.get_terminal_size()
            self.len = term_size.columns
        message = f"{self.prefix} {string}"[:self.len]
        width_count = get_east_asian_width_count(message)
        message = message[:self.len - width_count]
        print(message, end = end, file = file)

