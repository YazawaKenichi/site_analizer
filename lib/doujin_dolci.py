#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer

class DoujinDolci:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_description()
        self.update_category()
        self.update_tags()
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

    def update_title(self):
        tag = "h2"
        h2 = self.soup.find(tag)
        self.title = h2.text

    def update_description(self):
        tag = "div"
        class_ = "disc"
        div = self.soup.find(tag, class_ = class_)
        self.description = div.text

    def update_category(self):
        tag = "ul"
        class_ = "par_cat"
        ul = self.soup.find(tag, class_ = class_)
        li = ul.find("li")
        self.category = li.text

    def update_tags(self):
        tags = []
        tag = "ul"
        class_ = "tag"
        ul = self.soup.find(tag, class_ = class_)
        lis = ul.find_all("li")
        for li in lis:
            tags.append(li.text)
        self.tags = tags

    def update_srcs(self):
        hrefs = []
        tag = "div"
        class_ = "content"
        content = self.soup.find(tag, class_ = class_)
        anchors = content.find_all("a")
        for anchor in anchors:
            hrefs.append(anchor["href"])
        self.srcs = hrefs

    def update_sitename(self):
        self.sitename = "同人ドルチ"

