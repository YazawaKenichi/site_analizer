#!/usr/bin/env python3
# coding : utf-8
# Eromanga-Select

import SoupMaster as sm
import PathEditor as pe
import sys
from PrintMaster import Printer

class EromangaSelect:
    """ EromangaSelect class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.get(url)
        if self.ui:
            printer = Printer()
            config = { "name" : "EromangaSelect", "screen-full" : True}
            printer.setConfig(config)
            printer.print(f"Address : {self.url}")
            printer.print(f"Title : {self.title}")
            printer.print(f"Tags : {self.tags}")
            printer.print(f"Srcs : {self.src}")

    """ Get EromangaSelect Page """
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
        tag = "h2"
        class_ = None
        div = self.soup.find(tag, class_ = class_)
        self.title = div.text

    def update_tags(self):
        self.tags = sm.get_dict_html_to_python(self.soup, class_ = None, tag = "section")

    def update_src(self):
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
        self.src = _src

