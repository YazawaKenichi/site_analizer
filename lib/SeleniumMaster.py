#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: MIT License

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from PrintMaster import Printer
import argparse
import os, uuid

"""
from SeleniumMaster import Browser

initSelenium()
"""

class Browser:
    def __init__(self, options = None, browser = "/usr/bin/chromium-browser", driver = "/usr/bin/chromiumdriver", cookies = "./cookies.txt", ui = False):
        self.ui = ui
        self.browser_path = browser
        self.driver_path = driver
        self.cookies = cookies
        self.initSelenium(options)
        if self.ui:
            self.printer = Printer()
            self.config = {
                    "name" : "Browser",
                    "screen-full" : True
                    }
            self.printer.addConfig(self.config)

    # ブラウザを動かすためのクラスを作成する
    def initSelenium(self, options = None):
        import tempfile, shutil, atexit

        chrome_opts = Options()
        _tmp_profile = tempfile.mkdtemp(prefix = "selenium-profile-")
        chrome_opts.add_argument(f"--user-data-dir={_tmp_profile}")
        chrome_opts.add_argument("--no-first-run")
        chrome_opts.add_argument("--no-default-browser-check")
        chrome_opts.add_argument("--disable-background-networking")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--remote-debugging-port=0")

        if isinstance(options, dict):
            chrome_opts.add_experimental_option("prefs", options)

        if not self.ui:
            chrome_opts.add_argument("--headless=new")

        def _cleanup():
            try:
                shutil.rmtree(_tmp_profile, ignore_errors = True)
            except Exception:
                pass
        atexit.register(_cleanup)

        chrome_opts.binary_location = self.browser_path

        service = Service(executable_path = self.driver_path)
        self.driver = webdriver.Chrome(service = service, options = chrome_opts)
        self.wait = WebDriverWait(self.driver, 30)

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
        try:
            self.driver.quit()
        finally:
            try:
                if hasattr(self, "_tmp_profile"):
                    shutil.rmtree(self._tmp_profile, ignore_errors = True)
            except Exception:
                pass

    def screenshot(self, path):
        scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(1920, scroll_height)
        self.driver.save_screenshot(path)

