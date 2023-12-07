#!/usr/bin/env python3
# coding : utf-8
# ErodoujinshiWorld

import SoupMaster as sm
import PathEditor as pe
import sys
from PrintMaster import Printer

class ErodoujinshiWorld:
    """ ErodoujinshiWorld class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.tags = []
        self.src = []
        self.get(url)
        if self.ui:
            printer = Printer()
            config = { "name" : "ErodoujinshiWorld", "screen-full" : True}
            printer.setConfig(config)
            printer.print(f"Address : {self.url}")
            printer.print(f"Title : {self.title}")
            printer.print(f"Tags : {self.tags}")
            printer.print(f"Srcs : {self.src}")

    """ Get ErodoujinshiWorld Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_category()
        self.update_tags()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_category(self):
        li = self.soup.find("li", class_ = "post_category")
        self.category = li.text

    def update_title(self):
        tag = "h2"
        class_ = None
        div = self.soup.find(tag, class_ = class_)
        self.title = div.text

    def update_tags(self):
        tag = "li"
        id = None
        class_ = "post_tag"
        li = self.soup.find(tag, id = id, class_ = class_)
        anchors = li.find_all("a")
        for anchor in anchors:
            self.tags.append(anchor.text)

    def update_src(self):
        _src = []
        tag = "div"
        class_ = "kijibox"
        _srcs = sm.get_values_in_tag(self.soup, "div", "a", key = "href", class_ = "kijibox")
        for _src in _srcs:
            if pe.isimage(_src):
                self.src.append(_src)

