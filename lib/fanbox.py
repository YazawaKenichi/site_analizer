#!/usr/bin/env python3

from PrintMaster import Printer
from URLMaster import URL
import SoupMaster as sm
from SeleniumMaster import Browser
from urllib import parse

def save_soup(soup):
    import FDEditor as fde
    fde.create_file("fanbox.html", str(soup))

##### Post Page #####
class FanboxPost:
    def __init__(self, _url, cookies = None, browser = None, driver = None, headless = False, limit = 60, profile = None, port = 9222, verbose = False):
        self.verbose = verbose
        self.printer = Printer()
        config = { "name" : "FanboxPost", "screen-full" : True , "enable" : self.verbose}
        self.printer.addConfig(config)

        self.username = ""
        self.userid = ""
        self.srcs = []

        if isinstance(browser, Browser):
            self.browser = browser
        elif isinstance(browser, str):
            self.browser = Browser(options = None, browser = browser, driver = driver, cookies = cookies, headless = headless, limit = limit, profile = profile, port = port, verbose = self.verbose)
        else:
            raise TypeError(f"browser must be Browser or str, got {type(browser)}")

        self.update_url(_url)
        self.browser.openUrl(self.url, delay = 0.2)
        self.update_userid()

        self.update_soup()
        self.update_username()

        self.update_title()
        self.update_srcs()

        if self.verbose:
            self.printer.print(f"URL : {self.domain}, UserName : {self.username}", config = { "screen-full" : False })

    def update_url(self, _url):
        url = URL(_url)
        self.domain = url.domain
        self.url = url.basename
        if self.verbose:
            self.printer.print(f"Address : {self.url}")

    def update_userid(self):
        if URL(self.url).fqdn.split(".")[0] == "www":
            self.userid = URL(self.url).path.split("/")[0]
        else:
            self.userid = URL(self.browser.driver.current_url).fqdn.split(".")[0]

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        if self.verbose:
            self.printer.print(f"{self.url}", {"sub-name": "update_soup"})
        self.soup = self.browser.getSoup()

    def update_username(self):
        class_ = "UserNameText"
        a = sm.find_all_class_contains(self.soup, "a", class_)
        if a:
            self.username = a[0].text.strip()
        else:
            self.printer.print("class \"UserNameText\" is None")

    def update_title(self):
        class_ = "PostTitle"
        h1 = sm.find_all_class_contains(self.soup, "h1", class_)
        self.printer.print(f"{h1}", config = {"sub-name" : "update_title", "screen-full" : False})

    def update_srcs(self):
        class_ = "PostImage__Wrapper"
        divs = self.soup.find_all("div", class_ = class_)
        save_soup(self.soup)

        for div in divs:
            imgs = div.find_all("img")
            for img in imgs:
                src = img["src"]
                self.srcs.append(src)
                self.printer.print(f"{src}", config = {"sub-name" : "update_srcs"})

##### User Page #####
class FanboxUser:
    def __init__(self, _url, cookies = None, browser = None, driver = None, headless = False, limit = 60, profile = None, port = 9222, verbose = False):
        self.verbose = verbose
        self.printer = Printer()
        config = { "name" : "FanboxUser", "screen-full" : True , "enable" : self.verbose}
        self.printer.addConfig(config)

        self.username = ""
        self.userid = ""
        self.posturls = []

        if isinstance(browser, Browser):
            self.browser = browser
        elif isinstance(browser, str):
            self.browser = Browser(options = None, browser = browser, driver = driver, cookies = cookies, headless = headless, limit = limit, profile = profile, port = port, verbose = self.verbose)
        else:
            raise TypeError(f"browser must be Browser or str, got {type(browser)}")

        self.update_url(_url)
        self.browser.openUrl(self.url, delay = 0.2)
        self.update_userid()

        self.update_soup()
        self.update_username()
        self.update_posts()
        if self.verbose:
            self.printer.print(f"URL : {self.domain}, UserName : {self.username}", config = { "screen-full" : False })
        import FDEditor as fde
        fde.create_file("fanbox.html", str(self.soup))

    def update_url(self, _url):
        url = URL(_url)
        self.domain = url.domain
        self.url = url.basename
        if self.verbose:
            self.printer.print(f"Address : {self.url}")

    def update_userid(self):
        if URL(self.url).fqdn.split(".")[0] == "www":
            self.userid = URL(self.url).path.split("/")[0]
        else:
            self.userid = URL(self.browser.driver.current_url).fqdn.split(".")[0]

    def update_soup(self, browser = "/usr/bin/browser", driver = "/usr/bin/driver"):
        if self.verbose:
            self.printer.print(f"{self.url}", {"sub-name": "update_soup"})
        self.soup = self.browser.getSoup()

    def update_username(self):
        class_ = "UserNameText"
        a = sm.find_all_class_contains(self.soup, "a", class_)
        if a:
            self.username = a[0].text.strip()
        else:
            self.printer.print("class \"UserNameText\" is None")

    def update_posts(self):
        # 投稿タブの URL
        page = 1
        end = False
        while not end:
            new = 0
            posts_tab = parse.urljoin(self.domain, f"{self.userid}/posts") + "?sort=oldest" + f"&page={page}"
            # ページを開く
            self.browser.openUrl(posts_tab, delay = 0.2)
            soup = self.browser.getSoup()
            # 投稿一つ一つの URL を取得
            class_ = "CardPostItem__Wrapper"
            as_ = sm.find_all_class_contains(soup, "a", class_)
            for a in as_:
                posturl = parse.urljoin(self.domain, a["href"])
                if not posturl in self.posturls:
                    new += 1
                    self.posturls.append(posturl)
                    self.printer.print(f"{posturl}")
            if new == 0:
                end = True
            page += 1
            end = True

