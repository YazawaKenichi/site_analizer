#!/usr/bin/env python3
# coding : utf-8
# Shinshi-Manga

import sys
import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer

class Shinshi_Manga:
    """ Shinshi_Manga class """

    def __init__(self, url, ui = False):
        self.printer = Printer()
        config = {"name" : self.__class__.__name__, "screen-full" : True}
        self.printer.addConfig(config)
        self.get(url)
        self.notfound = False

    def get(self, url):
        self.update_url(url)
        self.update_uuid()
        self.update_tree()
        self.update_soup()
        self.update_title()
        self.update_descriptions()
        self.update_category()
        self.update_tag()
        self.update_pdf()

    def update_url(self, _url):
        self.url = URL(_url)

    def update_soup(self):
        self.prev_soup = sm.get_soup(self.preview.address, ui = False)
        self.binge_soup = sm.get_soup(self.binge.address, ui = False)
        self.dlpdf_soup = sm.get_soup(self.dlpdf.address, ui = False)

    def update_uuid(self):
        if ".pdf" in self.url.address.lower():
            _path = self.url.path
            _uuid = _path.split("/")[2]
        else:
            _uuid = self.url.param["uuid"]
        self.uuid = _uuid

    def update_tree(self):
        base_address = f"{self.url.scheme}://{self.url.fqdn}/comics/detail?uuid={self.uuid}"
        self.preview = URL(f"{base_address}&type=prev")
        self.binge = URL(f"{base_address}")
        self.dlpdf = URL(f"{base_address}&type=pdf")

    def update_title(self):
        top = self.prev_soup.find("div", class_ = "view__top")
        self.title = top.find("h1").text

    def update_descriptions(self):
        _div = self.prev_soup.find("div", class_ = "view__right")
        uls = _div.find_all("ul")
        _keys = ["原作", "キャラ", "タグ"]
        self.descriptions = {}
        for i, _key in enumerate(_keys):
            ufas = uls[i].find_all("li")
            _tmplist = []
            for ufa in ufas:
                _tmplist.append(ufa.text.replace("\n", "").replace(" ", ""))
            self.descriptions[_key] = _tmplist

    def update_category(self):
        self.category = self.descriptions["原作"][0]

    def update_tag(self):
        self.tag = self.descriptions["タグ"]

    def update_pdf(self):
        class_ = "btn__lg bc__blue"
        anchor = self.dlpdf_soup.find("a", class_ = class_)
        href = anchor["href"]
        self.pdf = f"{self.url.scheme}://{self.url.fqdn}{href}"

