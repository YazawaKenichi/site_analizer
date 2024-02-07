#!/usr/bin/env python3
# coding : utf-8
# PrintMaster

"""
printer = Printer()
config = {
    "name" : NAME,
    "sub-name" : SUBNAME,
    "len" : 32,
    "screen-full" : True
    }
printer.setConfig(config)
printer.print("Hello, World!")
"""

import sys
import shutil
import unicodedata
import copy

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
    KEYLIST = {"name" : None, "sub-name" : None, "len" : 65536, "screen-full" : False, "enable" : True}

    def __init__(self, name = None, enable = True):
        self.assignConfig(Printer.KEYLIST)
        config = {"name" : name, "enable" : enable}
        self.addConfig(config)

    # config 上書き / 新規作成
    def assignConfig(self, config):
        self.config = copy.deepcopy(Printer.KEYLIST)
        for k in config.keys():
            self.config[k] = config[k]
        self.updatePrefix()

    # config 追記
    def addConfig(self, config):
        for k in config.keys():
            self.config[k] = config[k]
        self.updatePrefix()

    # config 取得
    def getConfig(self):
        return self.config

    # prefix の更新
    def updatePrefix(self):
        self.name = self.config["name"]
        self.sub_name = self.config["sub-name"]
        self.len = self.config["len"]
        self.screen_full = self.config["screen-full"]
        self.enable = self.config["enable"]
        self.generatePrefix()

    # prefix の作成
    def generatePrefix(self):
        self.prefix = ""
        self.name_string = ""
        self.sub_string = ""
        if self.name is None:
            name_string = ""
        else:
            name_string = f"[{self.name}]"
        if self.sub_name is None:
            sub_string = ""
        else:
            sub_string = f"[{self.sub_name}]"
        self.prefix = f"{name_string}{sub_string}"

    def print(self, string, config = {}, end = "\r\n", file = sys.stdout, enable = None):
        buf = copy.deepcopy(self.getConfig())
        self.addConfig(config)

        if self.screen_full:
            term_size = shutil.get_terminal_size()
            self.len = term_size.columns
        message = f"{self.prefix} {string}"[:self.len]
        width_count = get_east_asian_width_count(message)
        message = message[:self.len - width_count]
        if (not enable is None) and (enable != self.enable):
            self.enable = enable
        if self.enable:
            print(message, end = end, file = file)

        self.assignConfig(buf)

