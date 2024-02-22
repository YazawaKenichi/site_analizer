#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
from URLMaster import URL
from PrintMaster import Printer
from PathEditor import isimage

class NijicollagePost:
    def __init__(self, url, ui = False):
        self.ui = ui
        self.update_printer()
        self.update_sitename()
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_notfound()
        if not self.notfound:
            self.update_tags()
            self.update_category()
            self.update_artist()
            self.update_descriptions()
            self.update_srcs()
            if self.ui :
                self.printer.print(f"{self.title}", config = {"sub-name" : "Title"})
                self.printer.print(f"{self.tags}", config = {"sub-name" : "Tags"})
                self.printer.print(f"{self.category}", config = {"sub-name" : "Category"})
                self.printer.print(f"{self.artist}", config = {"sub-name" : "Artist"})
                self.printer.print(f"{self.descriptions}", config = {"sub-name" : "Descriptions", "screen-full" : False})

    def update_printer(self):
        self.printer = Printer()
        config = { "name" : self.__class__.__name__, "screen-full" : True}
        self.printer.addConfig(config)

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    # タイトルの取得
    def update_title(self):
        ENTRY_TITLE = "entry-title"
        h1 = self.soup.find("h1", class_ = ENTRY_TITLE)
        self.title = h1.text

    # アーティスト（投稿者名）の取得
    def update_artist(self):
        self.artist = self.tags[0]

    # カテゴリの取得
    def update_category(self):
        self.category = self.tags[0]

    # 説明文の取得
    def update_descriptions(self):
        ENTRY_CONTENT = "entry-content"
        div = self.soup.find("div", class_ = ENTRY_CONTENT)
        """
        ps = div.find_all("p")
        for p in ps:
            self.descriptions = "".join(p.text) + "\r\n"
        """
        self.descriptions = div.text

    # タグの取得
    def update_tags(self):
        self.tags = []
        CATGROUP = "st-catgroup"
        p = self.soup.find("p", CATGROUP)
        anchors = p.find_all("a")
        for anchor in anchors:
            self.tags.append(anchor.text)

    def update_srcs(self):
        self.srcs = []
        ENTRY_CONTENT = "entry-content"
        div = self.soup.find("div", class_ = ENTRY_CONTENT)
        anchors = div.find_all("a")
        for anchor in anchors:
            src = anchor["href"]
            if isimage(src):
                self.srcs.append(src)

    def update_notfound(self):
        self.notfound = (self.title == " Hello! my name is 404 ")

    def update_sitename(self):
        self.sitename = "二次エロ素材倉庫♡虹こらこ"

class NijicollageCategory:
    def __init__(self, url, ui = False):
        self.ui = ui
        self.update_printer()
        self.update_sitename()
        self.update_url(url)
        self.update_soup()
        self.update_notfound()
        if not self.notfound:
            self.update_title()
            self.update_posts()

    def update_printer(self):
        self.printer = Printer()
        config = { "name" : self.__class__.__name__, "screen-full" : True}
        self.printer.addConfig(config)

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(self.url)

    # カテゴリ名を取得
    def update_title(self):
        self.title = self.soup.find("title").text.split(" - ")[-2]

    def update_posts(self):
        loop = True
        self.posts = []
        _url = self.url
        while loop:
            _soup = sm.get_soup(_url)
            div = _soup.find("div", class_ = "kanren")
            h3s = div.find_all("h3")
            for h3 in h3s:
                anchor = h3.find("a")
                self.posts.append(NijicollagePost(anchor["href"]))
            anchor = _soup.find("a", class_ = "next page-numbers")
            if not anchor is None:
                _url = anchor["href"]
            else:
                loop = False

    def update_notfound(self):
        _t = self.soup.find("h1", class_ = "entry-title").text
        self.notfound = (_t == " Hello! my name is 404 ")

    def update_sitename(self):
        self.sitename = "二次エロ素材倉庫♡虹こらこ"

