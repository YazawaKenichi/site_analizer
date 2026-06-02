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
import http.cookiejar

"""
from SeleniumMaster import Browser

initSelenium()
"""

class Browser:
    def __init__(self, options = None, browser = "/usr/bin/chromium-browser", driver = "/usr/bin/chromiumdriver", cookies = None, headless = False, limit = 30, profile = None, port = 9222, verbose = False):
        self.verbose = verbose
        self.headless = headless
        self.browser_path = browser
        self.driver_path = driver
        self.cookies = cookies
        self.cookies_loaded = False
        self.profile = profile
        self.port = port
        self.initSelenium(options, limit = limit, port = port)
        if self.verbose:
            self.printer = Printer()
            self.config = {
                    "name" : "Browser",
                    "screen-full" : True
                    }
            self.printer.addConfig(self.config)

    # ブラウザを動かすためのクラスを作成する
    def initSelenium(self, options = None, limit = 30, port = None):
        import tempfile, shutil, atexit

        chrome_opts = Options()

        def _cleanup():
            try:
                shutil.rmtree(_tmp_profile, ignore_errors = True)
            except Exception:
                pass

        if self.profile is None:
            _tmp_profile = tempfile.mkdtemp(prefix = "selenium-profile-")
            atexit.register(_cleanup)
        else:
            _tmp_profile = os.path.abspath(self.profile)
            chrome_opts.add_argument("--profile-directory=Default")
        chrome_opts.add_argument(f"--user-data-dir={_tmp_profile}")
        chrome_opts.add_argument("--no-first-run")
        chrome_opts.add_argument("--no-default-browser-check")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--remote-debugging-port=0")

        # chrome_opts.add_argument("--disable-background-networking")
        chrome_opts.add_argument("--disable-blink-features=AutomationControlled")
        chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_opts.add_experimental_option("useAutomationExtension", False)

        if not port is None:
            chrome_opts = Options()
            chrome_opts.debugger_address = f"127.0.0.1:{port}"

        if isinstance(options, dict):
            chrome_opts.add_experimental_option("prefs", options)

        if self.headless:
            chrome_opts.add_argument("--headless=new")

        atexit.register(_cleanup)

        chrome_opts.binary_location = self.browser_path

        service = Service(executable_path = self.driver_path)
        self.driver = webdriver.Chrome(service = service, options = chrome_opts)
        self.wait = WebDriverWait(self.driver, limit)

    def loadCookies(self, url = None):
        if not self.cookies:
            return
        jar = http.cookiejar.MozillaCookieJar(self.cookies)
        jar.load(ignore_discard = True, ignore_expires = True)
        if not url is None:
            self.driver.get(url)
        for c in jar:
            cookie = {
                    "name" : c. name,
                    "value" : c.value, 
                    "path" : c.path,
                    }
            if c.domain:
                cookie["domain"] = c.domain
            if c.expires:
                cookie["expiry"] = c.expires
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                if self.verbose:
                    self.printer.print(f"cookie skip: {c.name}: {e}", config = {"enable" : False})
        self.driver.refresh()

    # url のページを開く
    def openUrl(self, url, delay = None):
        if self.verbose:
            self.config["sub-name"] = "open"
            self.printer.print(url, config = self.config)
        # ブラウザでページを開く
        self.driver.get(url)
        if self.cookies and not self.cookies_loaded:
            self.loadCookies()
            self.cookies_loaded = True
        # ブラウザでページが開ききるのを待つ
        self.wait.until( lambda d: d.execute_script("return document.readyState") == "complete" )
        if delay:
            time.sleep(delay)

    # URL で指定したサイトの HTML を全て読み込ませてから取得する
    def getSoup(self):
        # HTML ソースを取得
        html = self.driver.page_source
        # bs4 型に作成
        soup = BeautifulSoup(html, "lxml")
        return soup

    def reload(self, num = "", verbose = True):
        self.driver.refresh()
        if self.verbose:
            self.config["sub-name"] = "reload"
            self.printer.print("refresh", config = self.config)

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

