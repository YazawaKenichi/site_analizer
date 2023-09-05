#!/usr/bin/env python3
# coding : utf-8

import re

def str2list(string, splitchar = " ", ui = True):
    list_ = string.split(splitchar)
    return list_

def delbrackets(string, prefix, suffix):
    return re.sub(f"{prefix}.*{suffix}",  "", string)

