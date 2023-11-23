#!/usr/bin/env python3
# coding : utf-8
# URLMaster

import re

class URL:
    """ URL Analizer """

    def __init__(self, url):
        self.get(url)

    def get(self, url):
        self.update_address(url)
        self.update_scheme()
        self.update_fqdn()
        self.update_path()
        self.update_param()
        self.update_flag()
        self.update_basename()
        self.update_domain()

    def update_address(self, url):
        self.address = url

    def update_scheme(self):
        self.scheme = self.address.split("://")[0]

    def update_fqdn(self):
        self.fqdn = self.address.split(f"{self.scheme}://")[1].split("/")[0]

    def update_path(self):
        _path = self.address.split(f"{self.scheme}://{self.fqdn}/")[1]
        self.path = re.split("[?#]", _path)[0]

    def update_param(self):
        _dict = {}
        if "?" in self.address:
            param_string = self.address.split("?")[1].split("#")[0]
            params = param_string.split("&")
            for param in params:
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

    """ 開発中 """
    def set_param(self, _param:dict):
        self.param = _param

