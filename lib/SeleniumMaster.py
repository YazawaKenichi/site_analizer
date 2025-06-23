#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: MIT License

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PrintMaster import Printer
import argparse

"""
from SeleniumMaster import Browser

initSelenium()
"""

class Browser:
    def __init__(self, options = None, browser = "/usr/bin/chromium-browser", driver = "/usr/bin/chromiumdriver", ui = False):
        self.ui = ui
        self.args, _ = self.__getArgs(browser, driver)
        self.driver_path = self.args.driver
        self.browser_path = self.args.browser
        self.cookies = self.args.cookies
        self.initSelenium(options)
        if self.ui:
            self.printer = Printer()
            self.config = {
                    "name" : "Browser",
                    "screen-full" : True
                    }
            self.printer.addConfig(self.config)

    def __getArgs(self, browser = "/usr/bin/chromium-browser", driver = "/usr/bin/chromiumdriver", cookies = "./cookies.txt"):
        parser = argparse.ArgumentParser(prog = "SeleniumMaster")
        parser.add_argument(
                "--driver",
                default = driver,
                type = str,
                dest = "driver",
                help = "chromiumdriver の場所",
                )
        parser.add_argument(
                "--browser",
                default = browser,
                type = str,
                dest = "browser",
                help = "chromium-browser の場所",
                )
        parser.add_argument(
                "--cookies",
                default = cookies,
                type = str,
                dest = "cookies",
                help = "cookies ファイルの場所",
                )
        return parser.parse_known_args()

    # ブラウザを動かすためのクラスを作成する
    def initSelenium(self, options = None):
        if options is None:
            options = Options()
        if not self.ui:
            options.add_argument("--headless")
        options.binary_location = self.browser_path
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
    def getSoup(self):
        # HTML ソースを取得
        html = self.driver.page_source
        # bs4 型に作成
        soup = BeautifulSoup(html, "lxml")
        return soup

    def reload(self, num = "", ui = True):
        self.driver.refresh()
        if self.ui:
            self.config["sub-name"] = "reload"
            self.printer.print("refresh")

    def close(self):
        self.driver.close()

    def screenshot(self, path):
        scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(1920, scroll_height)
        self.driver.save_screenshot(path)

