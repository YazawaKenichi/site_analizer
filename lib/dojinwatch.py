#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer
import PathEditor as pe

class DojinWatch:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_tags()
        self.update_artist_title_category()
        self.update_srcs()
        self.update_sitename()

        if ui :
            printer = Printer()
            config = { "name" : __class__.__name__, "screen-full" : False}
            printer.setConfig(config)
            config["sub-name"] = "Title"
            printer.setConfig(config)
            printer.print(self.title)
            config["sub-name"] = "Category"
            printer.setConfig(config)
            printer.print(self.category)
            config["sub-name"] = "Tags"
            printer.setConfig(config)
            printer.print(self.tags)

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    def update_tags(self):
        class_ = "kijibox"
        tag = "div"
        kijibox = sm.get_tags_from_class(self.soup, class_ = class_, tag = tag, ui = False)[0]
        ps = kijibox.find_all("p")
        text = ps[0].text

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
        hrefs = []
        tag = "div"
        class_ = "kijibox"
        kijibox = self.soup.find(tag, class_ = class_)
        ps = kijibox.find_all("p")[1:]
        for p in ps:
            anchor = p.find("a")
            if not anchor is None:
                hrefs.append(anchor["href"])
            else:
                img = p.find("img")
                key = "src"
                if not pe.isimage(img["src"]):
                    key = "data-lazy-src"
                hrefs.append(img[key])
        self.srcs = hrefs

    def update_sitename(self):
        self.sitename = "エロ同人ウオッチ"

