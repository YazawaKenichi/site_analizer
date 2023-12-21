#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer
from doujin_dolci import DoujinDolci

class NukiDokoro:
    def __init__(self, url, ui = False):
        self.update_url(url)
        self.update_soup()
        self.update_nopener()
        if not self.isNopener():
            self.update_tags()
            self.update_title()
            self.update_category()
            self.update_srcs()
            self.update_sitename()
        else:
            self.shift_dolci()

        if ui :
            printer = Printer()
            config = { "name" : "NukiDokoro", "screen-full" : False}
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

    def update_nopener(self):
        self.dolci = ""
        self.nopener = False
        tag = "div"
        class_ = "content"
        div = self.soup.find(tag, class_ = class_)
        data = [d for d in div.children]
        data = str(data[0:2])
        data = data.replace("\n", "")
        divs_head = sm.elementTag2BeautifulSoup(data)
        anchor = divs_head.find("a")
        if not anchor is None:
            href = anchor["href"]
            self.nopener = (anchor.text == "このサイトの記事を見る")
            self.dolci = href

    def update_tags(self):
        tags = []
        tag = "div"
        class_ = "single-post-category"
        divs = self.soup.find_all(tag, class_ = class_)
        for div in divs:
            tags.append(div.text)
        self.tags = tags

    def update_title(self):
        tag = "h1"
        class_ = "single-post-title entry-title"
        h1 = self.soup.find(tag, class_ = class_)
        self.title = h1.text

    def update_category(self):
        tag = "ul"
        id = "breadcrumb"
        ul = self.soup.find(tag, id = id)
        lis = ul.find_all("li")
        self.category = lis[1].text

    def update_srcs(self):
        srcs = []
        tag = "div"
        class_ = "content"
        content = self.soup.find(tag, class_ = class_)
        imgs = content.find_all("img")
        for img in imgs:
            srcs.append(img["src"])
        self.srcs = srcs

    def update_sitename(self):
        self.sitename = "抜き処"

    def shift_dolci(self):
        d = DoujinDolci(self.dolci)
        self.title = d.title
        self.category = d.category
        self.tags = d.tags
        self.srcs = d.srcs
        self.update_sitename()

    def isNopener(self):
        return self.nopener

