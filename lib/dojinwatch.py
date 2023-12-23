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
        self.update_descriptions()
        self.update_title()
        self.update_tags()
        self.update_category()
        self.update_srcs()
        self.update_sitename()
        self.notfound = False

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

    def update_descriptions(self):
        class_ = "kijibox"
        tag = "div"
        kijibox = sm.get_tags_from_class(self.soup, class_ = class_, tag = tag, ui = False)[0]
        ps = kijibox.find_all("p")
        text = ps[0].text

        tags = {}
        lines = text.split("\n")
        for line in lines:
            if ":" in line:
                li = line.split("：")
                key = li[0]
                val = li[1]
                tags[key] = val
        self.descriptions = tags

    def update_title(self):
        self.title = ""
        if "作品名" in self.descriptions.keys():
            self.title = self.descriptions["作品名"]
        else:
            _url = URL(self.url)
            self.title = _url.path.split("/")[-1]

    def update_tags(self):
        self.tags = []
        tag = "li"
        class_ = "post_tag"
        li = self.soup.find(tag, class_)
        anchors = li.find_all("a")
        for anchor in anchors:
            self.tags.append(anchor.text)

    def update_category(self):
        tag = "li"
        class_ = "post_category"
        li = self.soup.find(tag, class_ = class_)
        self.category = li.text

    def update_srcs(self):
        hrefs = []
        tag = "div"
        class_ = "kijibox"
        kijibox = self.soup.find(tag, class_ = class_)
        ps = kijibox.find_all("p")[1:]
        if not len(ps) == 0:
            for p in ps:
                anchors = p.find_all("a")
                for anchor in anchors:
                    if not anchor is None:
                        hrefs.append(anchor["href"])
                    else:
                        img = p.find("img")
                        key = "src"
                        if not pe.isimage(img["src"]):
                            key = "data-lazy-src"
                        hrefs.append(img[key])
        else:
            anchors = kijibox.find_all("a")
            for anchor in anchors:
                hrefs.append(anchor["href"])
        self.srcs = hrefs

    def update_sitename(self):
        self.sitename = "エロ同人ウオッチ"

