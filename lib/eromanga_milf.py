#!/usr/bin/env python3
# coding : utf-8
# Eromanga-Select

import SoupMaster as sm
import PathEditor as pe
import StdLib as sl
import sys
from PrintMaster import Printer

class EromangaMilf:
    """ EromangaMilf class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.tags = []
        self.src = []
        self.rensaku = []
        self.get(url)
        if self.ui:
            printer = Printer()
            config = { "name" : "EromangaMilf", "screen-full" : True}
            printer.setConfig(config)
            printer.print(f"Address : {self.url}")
            printer.print(f"Title : {self.title}")
            printer.print(f"Tags : {self.tags}")
            printer.print(f"Srcs : {self.src}")

    """ Get EromangaMilf Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_rensaku()
        self.update_title()
        self.update_category()
        self.update_tags()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url
    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_rensaku(self):
        div = self.soup.find("div", class_ = "box_rensaku")
        if not div is None:
            anchors = div.find_all("a")
            for anchor in anchors:
                self.rensaku.append(anchor["href"])
        else:
            self.rensaku = [self.url]

    def update_title(self):
        tag = "h1"
        class_ = "article-title entry-title"
        div = self.soup.find(tag, class_ = class_)
        self.title = div.text.replace("\n", "")

    def update_category(self):
        tag = "ul"
        class_ = "post-categories"
        ul = self.soup.find(tag, class_ = class_)
        li = ul.find("li")
        self.category = li.text

    def update_tags(self):
        tag = "div"
        class_ = "article-tags"
        self.tags = sm.get_list_html_to_python(self.soup, class_ = class_, tag = tag)

    def update_src(self):
        _src = []
        tag = "section"
        class_ = "entry-content"
        _srcs = sm.get_values_in_tag(self.soup, tag, "img", key = "src", class_ = class_)
        for __src in _srcs:
            if pe.isimage(__src):
                self.src.append(__src)

class EromangaMilfs:
    """ EromangaMilf class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.src = []
        self.milfs = []
        self.get(url)
        self.title = "test"
        if self.ui:
            printer = Printer()
            config = { "name" : "EromangaMilfs", "screen-full" : False}
            printer.setConfig(config)
            printer.print(f"Srcs : {self.src}")

    """ Get EromangaMilf Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_milf()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url
    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_milf(self):
        self.rensaku = EromangaMilf(self.url).rensaku
        self.milfs = [EromangaMilf(_milf, ui = self.ui) for _milf in self.rensaku]

    def update_src(self):
        for milf in self.milfs:
            self.src = sl.extend(self.src, milf.src)

