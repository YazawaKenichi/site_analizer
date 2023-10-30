#!/usr/bin/env python3
# coding : utf-8

import SoupMaster as sm
import os

class DDD_Smart:
    """ DDD-Smart class """

    def __init__(self, url):
        self.first = ""
        self.second = ""
        self.title = "".join(url.split("/")[3:5])
        self.get(url)
    
    """ Get Bestchai Page """
    def get(self, url):
        self.update_url(url)
        if "https://ddd-smart.net/doujinshi3/show-m.php" in self.url:
            self.update_soup()
            self.update_first()
        if "https://ddd-smart.net/dl-m-m.php" in self.url:
            self.update_soup()
            self.update_title()
            self.update_second()
        self.update_src()

    """ Update """
    def update_url(self, _url):
        self.url = _url

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui  = False)

    def update_title(self):
        tag = "h1"
        class_ = "list-pickup-header margin-bottom-0 card-panel white-text blue accent-2"
        self.title = sm.get_text_from_tag(self.soup, class_ = class_, tag = tag)

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
