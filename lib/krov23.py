#!/usr/bin/env python3
# coding : utf-8
# Krov23

import SoupMaster as sm
import PathEditor as pe
import sys
from PrintMaster import Printer
from URLMaster import URL

class Krov23:
    """ Krov23 Class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.printer = Printer()
        config = { "name" : __class__.__name__, "screen-full" : False}
        self.printer.setConfig(config)
        self.get(url)
        if self.ui:
            self.printer.print(f"Address : {self.url}")
            self.printer.print(f"Title : {self.title}")
            self.printer.print(f"Category : {self.category}")
            self.printer.print(f"Tags : {self.tags}")
            self.printer.print(f"Srcs : {self.srcs}")

    """ Get EromangaSelect Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_tags()
        self.update_srcs()
        self.update_sitename()
        self.update_category()

    """ Update """
    def update_url(self, _url):
        self.url = _url
    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_title(self):
        tag = "h2"
        class_ = None
        div = self.soup.find(tag, class_ = class_)
        self.title = div.text

    def update_tags(self):
        section = self.soup.find("section")
        trs = section.find_all("tr")
        td = trs[1].find("td")
        lis = td.find_all("li")
        self.tags = [t.text for t in lis]

    def update_srcs(self):
        _src = []
        tag = "div"
        id_ = "content"
        tags = sm.get_tags_from_id(self.soup, id_, tag = tag)
        h3 = sm.get_tags(tags[0], "h3")[0]
        __srcs = sm.get_image_urls(h3, None)
        for __src in __srcs:
            if pe.isimage(__src):
                tmp = __src.replace("\n", "")
                _src.append(tmp)
        self.srcs = _src

    def update_sitename(self):
        self.sitename = "エロ漫画セレクション"

    def update_category(self):
        self.category = URL(self.url).path.split("/")[0]
