#!/usr/bin/env python3
# coding : utf-8

from PrintMaster import Printer
from URLMaster import URL
import SoupMaster as sm
import FDEditor as fde
import os
from urllib import parse
import traceback

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

    def __init__(self, _url, browser = "/usr/bin/browser", driver = "/usr/bin/driver", headless = True, ui = False):
        self.printer = Printer()
        config = { "name" : "KemonoPost", "screen-full" : True }
        self.printer.addConfig(config)
        self.ui = ui
        self.headless = headless
        self.title = ""
        self.downloads = []
        self.content = ""
        self.content_urls = []
        self.files = []
        self.comments = {}
        self.update_url(_url)
        self.browser = browser
        self.driver = driver
        if self.ui:
            self.printer.print(f"Address : {self.url}")
        self.update_soup(self.browser, self.driver)
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
        if self.ui:
            self.printer.print(f"{self.url}", {"sub-name": "update_soup"})
        self.soup = sm.get_soup(self.url, on_browser = True, browser = browser, driver = driver, headless = self.headless, ui = self.ui)

    def update_artist(self):
        class_ = "post__user-name"
        a = self.soup.find("a", class_ = class_)
        self.artist = a.text.replace("\n", "").replace("\r", "").replace(" ", "")

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
        if not div is None:
            name_anchors = div.find_all("header", class_ = "fancy-link fancy-link--local comment__name")
            message_anchors = div.find_all("p", class_ = "comment__message")
            for index, name_anchor in enumerate(name_anchors):
                self.comments[name_anchor.text] = message_anchors[index].text
        else:
            self.comments["--- No Comments ---"] = ""

class KemonoPage:
    """ KemonoPage """
    def __init__(self, url, browser = "/usr/bin/browser", driver = "/usr/bin/driver", headless = True, ui = False):
        self.ui = ui
        self.printer = Printer()
        config = { "name" : "KemonoPage", "screen-full" : True }
        self.printer.addConfig(config)
        self.headless = headless
        self.browser = browser
        self.driver = driver
        self.get(url)

    def get(self, url):
        self.domain = URL(url).domain
        self.next = None
        self.posts = []
        self.update_url(url)
        self.update_soup(self.browser, self.driver)
        self.update_posts()
        self.update_next()

    def update_url(self, url):
        self.url = url

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        if self.ui:
            self.printer.print(f"{self.url}", {"sub-name": "update_soup"})
        self.soup = sm.get_soup(self.url, on_browser = True, browser = browser, driver = driver, headless = self.headless, ui = self.ui)

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
        bolds = self.soup.find_all(lambda tag: tag.name == "b" and tag.string == ">")
        anchor = bolds[0].parent
        class_list = anchor.get("class", [])
        if not "pagination-button-disabled" in class_list:
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

    def __init__(self, url, browser = "/usr/bin/browser", driver = "/usr/bin/driver", headless = True, ui = False):
        self.ui = ui
        self.headless = headless
        self.detail = True
        self.printer = Printer()
        config = { "name" : "Kemono", "screen-full" : True }
        self.printer.addConfig(config)
        self.browser = browser
        self.driver = driver
        self.get(url)

    """ Get Bestchai Page """
    def get(self, url):
        self.posts = []
        self.pages = []
        self.attribute_error_urls = []
        self.update_url(url)
        yet = 1
        while yet:
            self.update_soup(self.browser, self.driver)
            yet = self.update_meta()
        self.update_pages()
        self.update_posts()

    """ Update """
    def update_url(self, _url):
        self.url = URL(_url)
        if self.ui:
            self.printer.print(f"{self.url.address}", config = {"sub-name" : "update_url", "screen-full" : False})

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        if self.ui:
            self.printer.print(f"{self.url.basename}", {"sub-name": "update_soup"})
        self.soup = sm.get_soup(self.url.basename, on_browser = True, browser = browser, driver = driver, ui  = self.headless)
        # if self.ui:
        #     self.printer.print(f"{self.soup}", config = {"sub-name" : "update_soup", "screen-full" : False})

    def update_meta(self):
        head = self.soup.find("head")
        metas = head.find_all("meta")
        self.artist = None
        self.id = None
        self.service = None
        for meta in metas:
            try:
                meta_name = meta["name"]
                if ("artist_name" in meta_name):
                    self.artist = meta["content"]
                if ("id" in meta_name):
                    self.id = meta["content"]
                if ("service" in meta_name):
                    self.service = meta["content"]
            except KeyError as e:
                _ = 0
        if (not self.artist) or (not self.id) or (not self.service):
            self.printer.print(f"想定外の HTML ソースを取得したため再試行します: {self.url}", config = {"sub-name" : "update_posts", "screen-full" : True})
            return 1
        if self.ui:
            self.printer.print(f"Artist : {self.artist}", config = {"sub-name": "update_meta"})
            self.printer.print(f"Service : {self.service}", config = {"sub-name": "update_meta"})
            self.printer.print(f"ID : {self.id}", config = {"sub-name": "update_meta"})
        return 0

    def update_pages(self):
        exist_next = True
        address = self.url.basename
        while exist_next:
            self.pages.append(address)
            kemonopage = KemonoPage(address, browser = self.browser, driver = self.driver, headless = self.headless, ui = self.ui)
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
            kemonopage = KemonoPage(page, browser = self.browser, driver = self.driver, headless = self.headless, ui = self.ui)
            post_urls = extend(post_urls, kemonopage.posts)
        for post_url in post_urls:
            try:
                kemonopost = KemonoPost(post_url, browser = self.browser, driver = self.driver, headless = self.headless, ui = self.ui)
                self.posts.append(kemonopost)
            except AttributeError as e:
                traceback.print_exc()
                self.printer.print(f"想定外の HTML ソースを取得したためスキップします: {post_url}", config = {"sub-name" : "update_posts", "screen-full" : True})
                self.attribute_error_urls.append(post_url)

