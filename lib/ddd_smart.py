#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
import os

class DDD_Smart:
    """ DDD-Smart class """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.first = ""
        self.second = ""
        self.title = ""
        self.description = ""
        self.descriptions = {}
        self.category = ""
        self.get(url)
    
    """ Get Bestchai Page """
    def get(self, url):
        self.update_url(url)
        if "https://ddd-smart.net/doujinshi3/show-m.php" in self.url:
            self.update_soup()
            self.update_first()
        if "https://ddd-smart.net/dl-m-m.php" in self.url:
            self.update_soup()
            self.update_descriptions()
            self.update_description()
            self.update_title()
            self.update_category()
            self.update_second()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url
        if self.ui:
            print(self.url)

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_descriptions(self):
        _div = self.soup.find("div", class_ = "col s12 m12 l12")
        divs = _div.find_all("div", class_ = "detail-box")
        for div in divs:
            key = div.find("div", class_ = "head-box")
            val = div.find("div", class_ = "foot-box")
            k = " ".join(key.text.split())
            v = " ".join(val.text.split())
            self.descriptions[k] = v

    def update_category(self):
        self.category = self.descriptions["原作"]

    def update_title(self):
        self.title = self.description

    def update_description(self):
        tag = "h1"
        class_ = "list-pickup-header margin-bottom-0 card-panel white-text blue accent-2"
        self.description = sm.get_text_from_tag(self.soup, class_ = class_, tag = tag)

    def update_src(self):
        self.src = self.url

    def update_first(self):
        self.first = self.url
        class_ = "waves-effect btn-paging light-blue accent-4"
        tag_ = "li"
        prefix = "https://ddd-smart.net"
        lists = sm.get_hrefs_from_tag_in_anchor(self.soup, class_ = class_, tag = tag_, ui = False)
        self.update_url(f"{prefix}{lists[0]}")

    def update_second(self):
        self.second = self.url
        class_ = "waves-effect light-blue accent-4 dl-btn"
        tag_ = "div"
        prefix = ""
        lists = sm.get_hrefs_from_tag_in_anchor(self.soup, class_ = class_, tag = tag_, ui = False)
        self.update_url(f"{prefix}{lists[0]}")
