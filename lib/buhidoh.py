#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
import PathEditor as pe
import sys

class Buhidoh:
    """ Buhidoh class """

    def __init__(self, url):
        self.get(url)
    
    """ Get Bestchai Page """
    def get(self, url):
        self.update_url(url)
        self.update_soup()
        self.update_name()
        self.update_title()
        self.update_description()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_name(self):
        self.name = self.url.replace("https://buhidoh.net/blog-entry-d", "").replace(".html", "")

    def update_title(self):
        tag = "div"
        class_ = "ently_navi"
        div = self.soup.find(tag, class_ = class_)
        print(self.url)
        title_anchor = div.find_all("a")[1]
        self.title = title_anchor.text

    def update_description(self):
        text = ""
        tag = "h2"
        class_ = "ently_title"
        div = self.soup.find(tag, class_ = class_)
        if not div is None:
            text = div.text.replace("\n", "")
        self.description = text

    def get_anchor(self):
        hrefs = []
        div = self.soup.find(tag, class_ = class_)
        children = div.contents
        for child in children:
            try:
                hrefs.append(child["href"].replace("\n", ""))
            except:
                _ = 0
        return hrefs

    def update_src(self):
        _src = []
        class_ = "ently_text"
        tag = "div"
        for __src in sm.get_hrefs_from_tag_in_anchor(self.soup, class_, tag = tag):
            if pe.isimage(__src):
                _src.append(__src)
        self.src = _src[1:]
    