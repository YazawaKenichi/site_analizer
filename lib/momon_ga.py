#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from PrintMaster import Printer

class MomonGa:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_category()
        self.update_srcs()
        self.update_sitename()
        self.notfound = False

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    def update_title(self):
        h1 = self.soup.find("h1")
        self.title = h1.text

    def update_category(self):
        tag = None
        class_ = "post-tag-table"
        div = self.soup.find(tag = tag, class_ = class_)
        class_ = "post-tags"
        div = div.find("div", class_)
        self.category = div.text

    def update_srcs(self):
        id = "post-hentai"
        tag = "div"
        divs = sm.get_tags_from_id(self.soup, id, tag = tag)
        tags_ = []
        srcs = []
        for div in divs:
            tags_.extend(div.find_all("img"))
        for tag_ in tags_:
            srcs.append(tag_["src"])
        self.srcs = srcs

    def update_sitename(self):
        tag = None
        id = "logo"
        div = self.soup.find(tag = tag, id = id)
        self.sitename = div.text.replace(":", "-")

