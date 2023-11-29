#!/usr/bin/env python3
# coding : utf-8
# Turuweb

import SoupMaster as sm
import PathEditor as pe
from URLMaster import URL
import sys

class Turuweb:
    """ Turuweb class """

    def __init__(self, url):
        self.get(url)
    
    """ Get Turuweb Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_name()
        self.update_title_image()
        self.update_description()
        self.update_src()

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

    def update_name(self):
        tag = "h1"
        class_ = "single-article__title"
        h1 = self.soup.find(class_ = class_)
        self.name = "".join(h1.text.split())
        print(f"Name : {self.name}")

    def update_description(self):
        text = ""
        tag = ""
        class_ = ""

    def update_title_image(self):
        class_ = "single-article__img wp-post-image jetpack-lazy-image jetpack-lazy-image--handled".split()
        _titleimg = self.soup.find_all(class_ = class_)
        self.title_image_src = URL(_titleimg[0]["src"])
        print(f"Thumb : {self.title_image_src.basename}")

    def update_src(self):
        _src_ret = []
        _src = []
        # class_ = ["wp-block-image", "size-large"]
        # class_ = "alignnone jetpack-lazy-image jetpack-lazy-image--handled".split()
        class_ = "main__article single-article effect-item feadin".split()
        tag = "article"
        article = self.soup.find(class_ = class_)
        imgs = article.find_all("img")
        for img in imgs:
            apd = img["src"].replace("\n", "").split("?")[0]
            _src.append(apd)
        _srcs = _src
        for index, __src in enumerate(_srcs):
            if index % 2 == 0:
                _src_ret.append(__src)
        self.src = _src_ret[1:3+1]
        print(f"Page : {len(self.src)}")

