#!/usr/bin/env python3
# coding : utf-8
# Doujinnomori

import sys
import SoupMaster as sm
from URLMaster import URL

class Doujinnomori:
    """ Doujinnomori class """

    def __init__(self, url):
        self.get(url)
        self.notfound = False

    def get(self, url):
        self.update_url(url)
        self.update_uuid()
        self.update_tree()
        self.update_soup()
        self.update_title()
        self.update_tag()
        self.update_pdf()

    def update_url(self, _url):
        self.url = URL(_url)

    def update_soup(self):
        self.prev_soup = sm.get_soup(self.preview.address, ui = False)
        self.binge_soup = sm.get_soup(self.binge.address, ui = False)
        self.dlpdf_soup = sm.get_soup(self.dlpdf.address, ui = False)

    def update_uuid(self):
        if ".pdf" in self.url.address.lower():
            _path = self.url.path
            _uuid = _path.split("/")[2]
        else:
            _uuid = self.url.param["uuid"]
        self.uuid = _uuid

    def update_tree(self):
        base_address = f"{self.url.scheme}://{self.url.fqdn}/comics/detail?uuid={self.uuid}"
        self.preview = URL(f"{base_address}&type=prev")
        self.binge = URL(f"{base_address}")
        self.dlpdf = URL(f"{base_address}&type=pdf")

    def update_title(self):
        class_ = f"view__heading pc-none favorite_title_{self.uuid}"
        h1 = self.prev_soup.find("h1", class_ = class_)
        self.title = h1.text

    def update_tag(self):
        class_ = "tag pc-none"
        self.tag = ["".join(_tag.replace("\n", "").split()) for _tag in sm.get_list_html_to_python(self.prev_soup, class_ = class_)]

    def update_pdf(self):
        class_ = "button-more__item bgcolor__red"
        anchor = self.dlpdf_soup.find("a", class_ = class_)
        href = anchor["href"]
        self.pdf = f"{self.url.scheme}://{self.url.fqdn}{href}"

    def debug(self):
        print(f"Address :\n\tPreview : {self.preview.address}\n\tBinge : {self.binge.address}\n\tDLPDF : {self.dlpdf.address}\n{self.preview.debug()}{self.binge.debug()}{self.dlpdf.debug()}")


