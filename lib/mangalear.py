#!/usr/bin/env python3
# coding : utf-8
# Mangalear

import SoupMaster as sm
import PathEditor as pe
import sys
from PrintMaster import Printer

class Mangalear:
    """ Mangalear class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.notfound = False

        self.printer = Printer(self.ui)
        self.config = { "name" : "Mangalear", "screen-full" : False}
        self.printer.setConfig(self.config)

        self.tags = []
        self.srcs = []

        self.get(url)

    """ Get Mangalear Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        if not self.notfound:
            self.update_title()
            self.update_category()
            self.update_tags()
            self.update_srcs()
            self.update_sitename()

    """ Update """
    def update_url(self, _url):
        self.url = _url
        self.printer.print(f"Address : {self.url}")
    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)
        if not self.isNotFound() == "":
            self.notfound = True
            self.printer.print("404 Not Found")

    def update_title(self):
        tag = "h1"
        class_ = "entry-title"
        h1 = self.soup.find(tag, class_ = class_)
        self.title = h1.text.replace("\n", "")
        self.printer.print(f"Title : {self.title}")

    def update_category(self):
        span = self.soup.find("span", class_ = "category")
        anchor = span.find("a")
        self.category = anchor.text
        self.printer.print(f"Category : {self.category}")

    def update_tags(self):
        tag = "span"
        class_ = "post-tag"
        span = self.soup.find(tag, class_ = class_)
        anchors = span.find_all("a")
        for anchor in anchors:
            self.tags.append(anchor.text)
        self.printer.print(f"Tags : {self.tags}")

    def update_srcs(self):
        _src = []
        tag = "div"
        class_ = "entry-content"
        id = "the-content"
        _srcs = sm.get_values_in_tag(self.soup, tag, "a", key = "href", class_ = class_, id = id)
        for __src in _srcs:
            if pe.isimage(__src):
                self.srcs.append(__src)
        self.printer.print(f"Srcs : {self.srcs}")

    def isNotFound(self):
        text = ""
        h2 = self.soup.find("h2", class_ = "entry-title")
        if not h2 is None:
            text = h2.text
        return text

    def update_sitename(self):
        self.sitename = "同人まんがりあ"
