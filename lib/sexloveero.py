#!/usr/bin/env python3
# coding : utf-8
# sexloveero

import SoupMaster as sm
import PathEditor as pe
from URLMaster import URL
import sys

class SexLoveEro:
    """ SexLoveEro class """

    def __init__(self, url, ui = False):
        self.get(url)
        self.ui = ui
    
    """ Get SexLoveEro Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_notfound()
        if not self.notfound:
            self.update_title()
            self.update_description()
            self.update_srcs()

    """ SoupMaster Edit """
    def __get_image_urls_in_anchor_href_image_in_tag(self, class_, tag = "div"):
        __srcs = []
        __tags = self.soup.find_all(tag, class_ = class_)
        for __tag in __tags:
            __anchors = __tag.find_all("a")
            for __anchor in __anchors:
                if pe.isimage(str(__anchor["href"])):
                    __imgs = __anchor.find_all("img")
                    for __img in __imgs:
                        __srcs.append(str(__img["src"]))
        return __srcs

    """ Update """
    def update_url(self, _url):
        self.url = URL(_url)

    def update_soup(self):
        self.soup = sm.get_soup(self.url.address, parser = "lxml", ui  = False)

    def update_title(self):
        tag = "h1"
        class_ = "entry-title"
        h1 = self.soup.find(tag, class_ = class_)
        self.title = "".join(h1.text.split())
        # print(f"Title : {self.title}")

    def update_tags(self):
        span = self.soup.find("span", class_ = "cat-links")
        anchors = span.find_all("a")
        self.tags = [ v. for v in anchors ]

    def update_category(self):
        self.category = self.tags[0]

    def update_description(self):
        text = ""
        tag = ""
        class_ = ""

    def update_srcs(self):
        _srcs = []
        tag = "div"
        class_ = "entry-content"
        div = self.soup.find(tag, class_ = class_)
        ps = div.find_all("p", recursive = False)
        for p in ps:
            anchor = p.find("a", recursive = False)
            if not anchor is None:
                src = "".join(anchor["href"].replace("\n", "").split("?"))
                _srcs.append(src)
        self.srcs = _srcs
        # print(f"Page : {len(self.srcs)}")

    def update_notfound(self):
        tag = "h1"
        _class = "page-title"
        context = "このページは見つかりません。"
        h1 = self.soup.find(tag, class_ = _class)
        if not h1 is None:
            if context in h1.text.split():
                self.notfound = True
            else:
                self.notfound = False
        else:
            self.notfound = False

    def update_sitename(self):
        self.sitename = "エロ漫画雑誌特殊性癖"

