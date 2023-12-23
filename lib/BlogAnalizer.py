#!/usr/bin/env python3
# coding : utf-8

class BlogAnalizer:
    def __init__(self, url):
        self.title = ""
        self.update_url(url)
        self.update_soup()
        self.update_title()
        self.update_category()
        self.update_tags()
        self.update_artist()
        self.update_descriptions()
        self.update_comments()
        self.update_rensaku()

    def update_url(self, url):
        self.url = url

    def update_soup(self):
        self.soup = sm.get_soup(url)

