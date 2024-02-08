#!/usr/bin/env python3
# coding : utf-8
# Buhidoh

import SoupMaster as sm
import PathEditor as pe
import sys

class Buhidoh:
    """ Buhidoh class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.get(url)
    
    """ Get Bestchai Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        if not self.isNotFound():
            self.notfound = False
            self.update_category()
            self.update_description()
            self.update_title()
            self.update_srcs()
            self.update_sitename()
        else:
            self.notfound = True

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

    def isNotFound(self):
        title = self.soup.find("title")
        notfound = ("ページが見つかりませんでした" in title.text)
        return notfound

    """ Update """
    def update_url(self, _url):
        self.url = _url

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_title(self):
        self.title = self.url.replace("https://buhidoh.net/blog-entry-d", "").replace(".html", "")
        self.title = self.description

    def update_category(self):
        tag = "div"
        class_ = "ently_navi"
        div = self.soup.find(tag, class_ = class_)
        category_anchor = div.find_all("a")[1]
        self.category = category_anchor.text

    def update_description(self):
        text = ""
        tag = "h2"
        class_ = "ently_title"
        div = self.soup.find(tag, class_ = class_)
        if not div is None:
            text = div.text.replace("\n", "")
        self.description = text

    def update_srcs(self):
        _src = []
        class__ = "ently_text"
        tag = "div"
        __srcs = self.__get_image_urls_in_anchor_href_image_in_tag(class__, tag = tag)
        for __src in __srcs:
            if pe.isimage(__src):
                tmp = __src.replace("\n", "")
                _src.append(tmp)
        self.srcs = _src[1:]

    def update_sitename(self):
        self.sitename = "ぶひドウ！"
