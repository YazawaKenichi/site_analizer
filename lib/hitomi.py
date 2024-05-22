#!/usr/bin/env python3
# coding : utf-8
# hitomi.py

import SoupMaster as sm
from PrintMaster import Printer

class HitomiOnline:
    def __init__(self, url, ui = False):
        self.set_url(url)

    def set_url(self, url):
        self.url = url

    def set_soup(self):
        self.soup = sm.get_soup(self.url)

class HitomiPost:
    def __init__(self, url, ui = False):
        self.set_url(url)
        self.print = Printer(name = "Hitomi")
        config = {"name" : "Hitomi", "screen-full" : True}
        self.addConfig(config)
        self.ui = ui
        if self.ui:
            self.printer.print(f"Address : {self.url}")
        self.get_soup()
        if self.ui:
            self.printer.print(self.soup)

    def set_url(self, url):
        self.url = url

    def get_soup(self):
        self.soup = sm.get_soup(self.url)

    def get_title(self):
        self.title = ""
        h1 = self.soup.find("h1", id = "gallery-brand")
        self.title = h1.text

    def get_artists(self):
        self.artists = []
        h2 = self.soup.find("h2", id = "artists")
        lis = h2.find_all("li")
        for li in lis:
            self.artists.append(li.text)

    def get_online(self):
        self.srcs = []
        a = self.soup.find("a", id = "read-online-button")
        href = a["href"]
        online = HitomiOnline("https://hitomi.la" + href)

    def get_series(self):
        self.series = ""

    def get_characters(self):
        self.characters = []

    def get_tags(self):
        self.tags = []


