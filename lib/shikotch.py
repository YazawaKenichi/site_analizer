#!/usr/bin/env python3
# coding : utf-8
# Eromanga-Select

import SoupMaster as sm
import PathEditor as pe
import sys
from PrintMaster import Printer

class Shikotch:
    """ Shikotch class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.tags = []
        self.get(url)
        if self.ui:
            printer = Printer()
            config = { "name" : "Shikotch", "screen-full" : True}
            printer.setConfig(config)
            printer.print(f"Address : {self.url}")
            printer.print(f"Title : {self.title}")
            printer.print(f"Tags : {self.tags}")
            printer.print(f"Srcs : {self.src}")

    """ Get Shikotch Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_tags()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url
    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_title(self):
        tag = "h1"
        class_ = None
        div = self.soup.find(tag, class_ = class_)
        self.title = div.text

    def update_tags(self):
        span = self.soup.find("span", id = "post-tag")
        anchors = span.find_all("a")
        for anchor in anchors:
            self.tags.append(anchor.text)

    def update_src(self):
        _src = []
        tag = "div"
        id_ = "post-comic"
        __srcs = sm.get_image_urls_in_tag(self.soup, tag, id_ = id_)
        for __src in __srcs:
            if pe.isimage(__src):
                tmp = __src.replace("\n", "")
                _src.append(tmp)
        self.src = _src

