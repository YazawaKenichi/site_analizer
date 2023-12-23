#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer

class EromangaCeleb:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_artist()
        self.update_title()
        self.update_category()
        self.update_srcs()
        self.update_sitename()
        self.notfound = False

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    def update_artist(self):
        url = URL(self.url)
        self.artist = url.path.split("/")[0]

    def update_title(self):
        self.title = self.soup.find("h2").text

    def update_category(self):
        self.category = self.artist

    def update_srcs(self):
        srcs = []
        class_ = "article_inner"
        div = self.soup.find(class_ = class_)
        p = div.find("p")
        anchors = p.find_all("a")
        for anchor in anchors:
            srcs.append(anchor["href"])
        self.srcs = srcs

    def update_sitename(self):
        self.sitename = "エロ漫画セレブ"

