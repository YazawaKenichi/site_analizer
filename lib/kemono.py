#!/usr/bin/env python3
# coding : utf-8

from PrintMaster import Printer
from URLMaster import URL
import SoupMaster as sm
import FDEditor as fde
import os
from urllib import parse

def extend(lista, listb):
    ret = []
    for lista_ in lista:
        ret.append(lista_)
    for listb_ in listb:
        ret.append(listb_)
    return ret

class KemonoPost:
    """ KemonoPost class """

    """
    str url
    BeautifulSoup soup
    str title
    str[] downloads
    str content
    str[] files
    str{} comments
    """

    def __init__(self, _url, ui = False):
        self.printer = Printer()
        config = { "name" : "KemonoPost", "screen-full" : True }
        self.printer.addConfig(config)
        self.ui = ui
        self.title = ""
        self.downloads = []
        self.content = ""
        self.content_urls = []
        self.files = []
        self.comments = {}
        self.update_url(_url)
        if self.ui:
            self.printer.print(f"Address : {self.url}")
        self.update_soup()
        self.update_artist()
        self.update_title()
        self.update_downloads()
        self.update_content()
        self.update_files()
        self.update_comments()
        if self.ui:
            self.printer.print(f"Artist : {self.artist}, Title : {self.title}, Downloads : {len(self.downloads)}, Files : {len(self.files)}")

    def update_url(self, _url):
        url = URL(_url)
        self.domain = url.domain
        self.url = url.basename

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        self.soup = sm.get_soup(self.url, on_browser = True, browser = browser, ui = False)

    def update_artist(self):
        class_ = "post__user-name"
        a = self.soup.find("a", class_ = class_)
        try:
            self.artist = a.text.replace("\n", "").replace("\r", "").replace(" ", "")
        except AttributeError:
            import sys
            print("URL")
            print(self.url)
            print("AttributeError")
            print(self.soup)
            fde.create_file("./errorpage.html", self.soup)
            sys.exit(0)

    def update_title(self):
        h1 = self.soup.find("h1", class_ = "post__title")
        if not h1 is None:
            span = h1.find("span")
            self.title = span.text
        else:
            _name = URL(self.url).path.split("/")[-1]
            fde.create_file(_name + ".html", str(self.soup))
            printer.print(f"Output : {_name}")
            sys.exit(0)

    def update_downloads(self):
        lists = self.soup.find_all(class_ = "post__attachment-link")
        for li in lists:
            tmp = str(li.text).split()
            filetitle = tmp[1]
            self.downloads.append(str(li['href']))

    def update_content(self):
        div = self.soup.find(class_ = "post__content")
        if not div is None:
            self.content = div.text
            anchors = div.find_all("a")
            for anchor in anchors:
                if URL(anchor["href"]).is_url:
                    self.content_urls.append(anchor["href"])
                    # self.printer.print(f"{self.content_urls[-1]}", config = {"sub-name" : "Update Content"})
            imgs = div.find_all("img")
            for img in imgs:
                self.content_urls.append(parse.urljoin(self.domain, img["src"]))
                # self.printer.print(f"{self.content_urls[-1]}", config = {"sub-name" : "Update Content"})

    def update_files(self):
        divs = self.soup.find_all("div", class_ = "post__files")
        for div in divs:
            imgs = div.find_all('img')
            anchors = div.find_all("a")
            for img in imgs:
                self.files.append(parse.urljoin(URL(self.url).scheme + ":", img["src"]))
            for anchor in anchors:
                self.files.append(anchor["href"])

    def update_comments(self):
        div = self.soup.find(class_ = "post__comments")
        name_anchors = div.find_all("header", class_ = "fancy-link fancy-link--local comment__name")
        message_anchors = div.find_all("p", class_ = "comment_message")
        for index, name_anchor in enumerate(name_anchors):
            self.comments[name_anchor.text] = message_anchors[index].text

class KemonoPage:
    """ KemonoPage """
    def __init__(self, url):
        self.get(url)

    def get(self, url):
        self.domain = URL(url).domain
        self.next = None
        self.posts = []
        self.update_url(url)
        self.update_soup()
        self.update_posts()
        self.update_next()

    def update_url(self, url):
        self.url = url

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        self.soup = sm.get_soup(self.url, on_browser = True, browser = browser, ui = False)

    def update_posts(self):
        articles = self.soup.find_all(class_ = "post-card")
        for article in articles:
            for in_article in article.children:
                if(in_article.name != None):
                    if(in_article.name == 'a'):
                        address = self.domain + str(in_article["href"])
                        self.posts.append(address)
        self.posts.reverse()

    def update_next(self):
        anchor = self.soup.find(class_ = "fancy-link fancy-link--kemono next")
        if not anchor is None:
            self.next = self.domain + anchor["href"]

class Kemono:
    """ Kemono class """

    """
    URL url
    BeautifulSoup soup
    str id
    str service
    str artist
    str[] pages
    KemonoPost[] posts
        str url
        BeautifulSoup soup
        str title
        str[] downloads
        str content
        str[] files
        str{} comments
    """

    def __init__(self, url, ui = False):
        self.ui = ui
        self.detail = True
        self.printer = Printer()
        config = { "name" : "Kemono", "screen-full" : True }
        self.printer.addConfig(config)
        self.get(url)

    """ Get Bestchai Page """
    def get(self, url):
        self.posts = []
        self.pages = []
        self.update_url(url)
        self.update_soup()
        self.update_meta()
        self.update_pages()
        self.update_posts()

    """ Update """
    def update_url(self, _url):
        self.url = URL(_url)
        if self.ui:
            self.printer.print(f"{self.url.address}", config = {"sub-name" : "update_url", "screen-full" : False})

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        self.soup = sm.get_soup(self.url.basename, on_browser = True, browser = browser, ui  = False)
        if self.ui:
            self.printer.print(f"{self.soup}", config = {"sub-name" : "update_soup", "screen-full" : False})

    def update_meta(self):
        head = self.soup.find("head")
        metas = head.find_all("meta")
        self.id = metas[2]["content"]
        self.service = metas[3]["content"]
        self.artist = metas[4]["content"]

    def update_pages(self):
        exist_next = True
        address = self.url.basename
        while exist_next:
            self.pages.append(address)
            kemonopage = KemonoPage(address)
            address = kemonopage.next
            if address is None:
                exist_next = False
            if self.ui:
                self.printer.print(f"Next Page Address : {address}", config = {"sub-name" : "update_pages", "screen-full" : True})
                self.printer.print(f"Exist Next : {exist_next}", config = {"sub-name" : "update_pages", "screen-full" : True})
        self.pages.reverse()

    def update_posts(self):
        post_urls = []
        for page in self.pages:
            kemonopage = KemonoPage(page)
            post_urls = extend(post_urls, kemonopage.posts)
        for post_url in post_urls:
            kemonopost = KemonoPost(post_url, ui = self.ui)
            self.posts.append(kemonopost)

