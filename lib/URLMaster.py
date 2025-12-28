#!/usr/bin/env python3
# coding : utf-8
# URLMaster

import re
from urllib.parse import unquote
from sys import stderr

class URL:
    """ URL Analizer """

    """
    _url = "https://www.example.com/dir1/dir2/file.ex?key1=val1&key2=val2&key3=val3#flag
    url = URL(_url)
    "https://www.example.com/dir1/dir2/file.ex?key1=val1&key2=val2&key3=val3#flag" = url.address
    "https" = url.scheme
    "www.example.com"= url.fqdn
    "dir1/dir2/file.ex" = url.path
    {"key1" : "val1", "key2" : "val2"} = url.param
    "flag" = url.flag
    "https://www.example.com/dir1/dir2/file.ex" = url.basename
    "https://www.example.com" = url.domain
    """

    def __init__(self, url, verbose = False):
        self.verbose = verbose
        self.get(url)

    def get(self, url):
        self.update_address(url)
        self.isURL(url)
        if self.is_url:
            self.update_scheme()
            self.update_fqdn()
            self.update_path()
            self.update_param()
            self.update_flag()
            self.update_basename()
            self.update_domain()
        else:
            if self.verbose:
                print(f"[URLMaster][isURL] Invalied URL : {url}")

    def update_address(self, url):
        self.address = unquote(url)

    def update_scheme(self):
        self.scheme = self.address.split("://")[0]

    def update_fqdn(self):
        self.fqdn = self.address.split(f"{self.scheme}://")[1].split("/")[0]

    def update_path(self):
        try:
            _path = self.address.split(f"{self.scheme}://{self.fqdn}/")[1]
            self.path = re.split("[?#]", _path)[0]
            return 0
        except IndexError:
            print(f"[URLMaster][URL][update_path] IndexError")
            print(f"[URLMaster][URL][update_path] Address : {self.address}")
            self.path = ""
            return 1

    def update_param(self):
        _dict = {}
        if "?" in self.address:
            param_string = self.address.split("?")[1].split("#")[0]
            params = param_string.split("&")
            for param in params:
                if "=" in param:
                    key = param.split("=")[0]
                    val = param.split("=")[1]
                    _dict[key] = val
        self.param = _dict

    def update_flag(self):
        _flag = ""
        if "#" in self.address:
            _flag = self.address.split("#")[-1]
        self.flag = _flag

    def update_basename(self):
        self.basename = f"{self.scheme}://{self.fqdn}/{self.path}"

    def update_domain(self):
        self.domain = f"{self.scheme}://{self.fqdn}"

    def debug(self):
        print(f"Address : {self.address}\n\tScheme : {self.scheme}\n\t FQDN  : {self.fqdn}\n\t path  : {self.path}\n\tparam  : {self.param}\n\t flag  : {self.flag}")

    def isURL(self, text):
        url_pattern = re.compile(
            r'^(http|https)://'  # protocol
            r'([0-9a-zA-Z.-]+)'  # domain
            r'(\.[a-zA-Z]{2,})'   # top-level domain
            r'(/[^\s]*)?'        # path
            r'$'
            )
        self.is_url = bool(url_pattern.match(text))

    """ 開発中 """
    def set_param(self, _param:dict):
        self.param = _param

