#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer

class EromangaLife:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_tags()
        self.update_artist_title_category()
        self.update_srcs()
        self.update_sitename()
        if ui :
            printer = Printer()
            config = { "name" : "EromangaLife", "screen-full" : True}
            printer.setConfig(config)
            printer.print(tags)

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    def update_tags(self):
        class_ = "entry-content"
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
        if "作者名" in self.tags.keys():
            self.artist = self.tags["作者名"]
        elif "サークル名" in self.tags.keys():
            self.artist = self.tags["サークル名"]
        if "作品名" in self.tags.keys():
            self.title = self.tags["作品名"]
        else:
            self.title = URL(self.url).path.split(".")[-2]
        self.category = self.tags["元ネタ"]

    def update_srcs(self):
        tag = "div"
        class_ = "entry-content"
        hrefs = []
        div = self.soup.find(tag, class_)
        ps = div.find_all("p")[1:]
        for p in ps:
            a = p.find("a")
            if not a is None:
                hrefs.append(a["href"])
            else:
                img = p.find("img")
                hrefs.append(img["src"])
        self.srcs = hrefs

    def update_sitename(self):
        self.sitename = "エロ漫画ライフ"

