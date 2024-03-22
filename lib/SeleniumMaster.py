#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: MIT License

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PrintMaster import Printer
from optparse import OptionParser

class Browser:
    def __init__(self, browser = "/usr/bin/chromium-browser", driver = "/usr/bin/chromiumdriver", ui = False):
        self.ui = ui
        browser = self.getArgs()
        self.initSelenium(browser, ui)
        if self.ui:
            self.printer = Printer()
            self.config = {
                    "name" : "Browser",
                    "screen-full" : True
                    }
            self.printer.setConfig(self.config)

    def getArgs(self):
        parser = OptionParser()
        parser.add_option(
                "--driver",
                default = "/usr/bin/chromiumdriver",
                type = "string",
                dest = "driver",
                help = "chromiumdriver の場所"
                )
        parser.add_option(
                "--browser",
                default = "/usr/bin/chromium-browser",
                type = "string",
                dest = "browser",
                help = "chromium-browser の場所"
                )
        return parser.parse_args()

    # ブラウザを動かすためのクラスを作成する
    def initSelenium(self, browser = "/usr/bin/chromium-browser", driver = "/usr/bin/chromiumdriver"):
        options = Options()
        if not self.ui:
            options.add_argument("--headless")
        options.binary_location = browser
        self.driver = webdriver.Chrome(options = options)

    # url のページを開く
    def openUrl(self, url, delay = 10):
        if self.ui:
            self.config["sub-name"] = "open"
            self.printer.print(url)
        # ブラウザでページを開く
        self.driver.get(url)
        # ブラウザでページが開ききるのを待つ
        time.sleep(delay)

    # URL で指定したサイトの HTML を全て読み込ませてから取得する
    def getSoup(self, cookies = None):
        # HTML ソースを取得
        html = self.driver.page_source
        # bs4 型に作成
        soup = BeautifulSoup(html, "lxml", cookies = cookies)
        return soup

    def reload(self, num = "", ui = True):
        self.driver.refresh()
        if self.ui:
            self.config["sub-name"] = "reload"
            self.printer.print("refresh")

    def close(self):
        self.driver.close()

