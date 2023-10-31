#!/usr/bin/env python3
# coding : utf-8
# Bestchai

import SoupMaster as sm

class Bestchai:
    """ Bestchai class """

    def __init__(self, url):
        self.get(url)
    
    """ Get Bestchai Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_title(self):
        tag = "h1"
        class_ = "article-title entry-title"
        element = self.soup.find(tag, class_ = class_)
        title_anchor = element.find("a")
        self.title = title_anchor

    def update_src(self):
        class_ = ["alignnone", "size-full"]
        srcs = []
        imgs = self.soup.find_all("img", class_= class_)
        for img in imgs:
            srcs.append("https:" + str(img["src"]))
        self.src = srcs
    
