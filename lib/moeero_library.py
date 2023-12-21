#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from PrintMaster import Printer

class MoeeroLibrary:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_tags()
        self.update_artist_title_category()
        self.update_srcs()
        self.update_sitename()

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    def update_tags(self):
        class_ = "kijibox"
        tag = "div"
        lists = sm.get_tags_from_class(self.soup, class_ = class_, tag = tag, ui = False)
        p = lists[0].find("p")
        text = p.text

        tags = {}
        lines = text.split("\n")
        for line in lines:
            li = line.split("：")
            key = li[0]
            val = li[1]
            tags[key] = val
        self.tags = tags

    def update_artist_title_category(self):
        self.artist = self.tags["作者名"]
        self.title = self.tags["作品名"]
        self.category = self.tags["元ネタ"]

    def update_srcs(self):
        tag = "div"
        class_ = "kijibox"
        hrefs = []
        div = self.soup.find(tag, class_)
        ps = div.find_all("p")[1:]
        for p in ps:
            a = p.find("a")
            hrefs.append(a["href"])
        self.srcs = hrefs

    def update_sitename(self):
        self.sitename = "萌えエロ図書館"

