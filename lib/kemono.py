#!/usr/bin/env python3
# coding : utf-8

from PrintMaster import Printer
from URLMaster import URL
import SoupMaster as sm
import os

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
        self.ui = ui
        self.title = ""
        self.downloads = []
        self.content = ""
        self.files = []
        self.comments = {}
        self.get(_url)
        if self.ui:
            printer = Printer()
            config = { "name" : "KemonoPost", "screen-full" : True }
            printer.setConfig(config)
            printer.print(f"Address : {self.url}")
            printer.print(f"Title : {self.title}, Downloads : {len(self.downloads)}, Files : {len(self.files)}")

    def get(self, _url):
        self.update_url(_url)
        self.update_soup()
        self.update_title()
        self.update_downloads()
        self.update_content()
        self.update_files()
        self.update_comments()

    def update_url(self, _url):
        url = URL(_url)
        self.domain = url.domain
        self.url = url.basename

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui = False)

    def update_title(self):
        h1 = self.soup.find(class_ = "post__title")
        span = h1.find("span")
        self.title = span.text

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

    def update_files(self):
        anchor_class = ['fileThumb', 'image-link']
        anchors = self.soup.find_all(class_ = anchor_class[0])
        for anchor in anchors:
            img = anchor.find('img')
            address = f"https:{str(img['src'])}"
            self.files.append(address)

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

    def update_soup(self):
        self.soup = sm.get_soup(self.url, ui = False)

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
        anchor = self.soup.find(class_ = "next")
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
        self.get(url)
        if self.ui:
            printer = Printer()
            config = { "name" : "Kemono", "screen-full" : True }
            printer.setConfig(config)
            printer.print(f"[Kemono] Address : {self.url.address}")
            printer.print(f"[Kemono] ID : {self.id}, Service : {self.service}, Artist : {self.artist}")
            printer.print(f"[Kemono] Pages : {len(self.pages)}")

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

    def update_soup(self):
        self.soup = sm.get_soup(self.url.basename, ui  = False)

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

    def update_posts(self):
        post_urls = []
        for page in self.pages:
            kemonopage = KemonoPage(page)
            post_urls = extend(post_urls, kemonopage.posts)
        for post_url in post_urls:
            kemonopost = KemonoPost(post_url, ui = self.ui)
            self.posts.append(kemonopost)
