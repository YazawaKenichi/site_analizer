#!/usr/bin/env python3
# coding : utf-8
# Bestchai

import SoupMaster as sm

class Bestchai:
    """ Bestchai class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.get(url)
    
    """ Get Bestchai Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_srcs()
        self.update_sitename()
        self.update_category()

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
        self.title = title_anchor.text

    def update_srcs(self):
        class_ = ["alignnone", "size-full"]
        _srcs = []
        imgs = self.soup.find_all("img", class_= class_)
        for img in imgs:
            _srcs.append("https:" + str(img["src"]))
        self.srcs = _srcs
    
    def update_sitename(self):
        self.sitename = "エロ漫画の馬小屋"

    def update_category(self):
        tag = "ul"
        class_ = "post-categories"
        ul = self.soup.find(tag, class_ = class_)
        self.category = ul.text.replace("\n", "")
