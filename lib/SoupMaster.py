#!/usr/bin/env python3
# coding: utf-8
# SoupMaster.py
# HTML を操作

import datetime
import time
import urllib
from urllib import request
import chardet
from bs4 import BeautifulSoup
import bs4
import requests
import sys
import cv2
import tempfile
from PIL import Image, ImageFile, UnidentifiedImageError
import ImageEditor as ie
import FDEditor as fde
import io
import os
import numpy as np
from PrintMaster import Printer
from SeleniumMaster import Browser

# アドレスの BeautifulSoup を返す
def get_soup(address, parser = "html.parser", cookies = None, on_browser = False, browser = "/usr/bin/browser", driver = "/usr/bin/driver", ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "get_soup", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    if on_browser:
        browser = Browser(browser = browser, driver = driver)
        browser.openUrl(address)
        soup = browser.getSoup()
        browser.close()
        return soup
    else:
        try:
            # ユーザエージェントの偽装
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            headers = getHeaders()
            # レスポンスの情報を管理するオブジェクトを返す
            # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
            with requests.get(address, headers = headers, cookies = cookies) as response:
                time.sleep(0.5)
                # 取得した文字列をまとめて取り出す
                body = response.content
                data = body
                if ui:
                    printer.print("[open] " + address)
                soup = BeautifulSoup(data, parser)
                return soup
        except requests.exceptions.ConnectionError as rece:
            if ui :
                print("\x1b[31m" + address + " : Connection aborted!\r\nRemote Disconnected\r\nRemote end closed connection without response." + "\x1b[0m", file = sys.stderr)
            time.sleep(5)
            get_soup(address, ui)
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            if ui :
                printer.print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
            time.sleep(0.5)
            get_soup(address, ui)

def list2soup(_list, ui = False):
    li = "".join(map(str, _list))
    soup = BeautifulSoup(li, "html.parser")
    return soup

def str2soup(string, ui = False):
    soup = BeautifulSoup(str(string), "html.parser")
    return soup

def print_element(elem):
    config = {"name" : "SoupMaster", "sub-name" : "print_element", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    if isinstance(elem, bs4.NavigableString):
        printer.print(type(elem), elem.string)
    else:
        printer.print(type(elem), elem.name)

def get_tags(soup, tag = "div"):
    list_ = soup.find_all(tag)
    return list_

# 特定クラス名を持つタグの要素を取得
def get_tags_from_class(soup, class_, tag = "div", ui = False):
    lists = soup.find_all(tag, class_ = class_)
    return lists

# 特定の ID 名を持つタグの要素を取得
def get_tags_from_id(soup, id, tag = "div", ui = False):
    lists = soup.find_all(tag, id = id)
    return lists

# <a class = anchor_class href = "***" ></a>
def get_hrefs(soup, anchor_class, ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "get_hrefs", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    lists = soup.find_all(class_ = anchor_class)
    hrefs = []
    for li in lists:
        hrefs.append(str(li['href']))
        if ui:
            printer.print("[append] " + str(li['href']))
    return hrefs

# <tag class = tag_class><a href = "***"></a></tag>
def get_hrefs_from_tag_in_anchor(soup, class_, tag = "div", recursion = True, ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "get_hrefs_from_tag_in_anchor", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    # tag_class を持つ tag のリストを取得する
    lists = get_tags_from_class(soup, class_ = class_, tag = tag, ui = ui)
    hrefs = []
    for li in lists:
        anchors = []
        anchors = li.find_all("a")
        for anchor in anchors:
            hrefs.append(str(anchor['href']))
    if ui:
        printer.print("[get] ", lists)
    return hrefs

# <tag class = tag_class> **** </tag>
def get_text_from_tag(soup, class_, tag = "div", ui = False):
    element = soup.find(tag, class_ = class_)
    return element.text

# bs4.BeautifulSoup 型にして返す
def elementTag2BeautifulSoup(data, ui = False):
    string = ""
    string = str(data)
    soup = BeautifulSoup(string, 'lxml')
    return soup

# href があるかどうかを判断する
def exist_href(soup, anchor_class, ui = False):
    hrefs = get_hrefs(soup, anchor_class, ui = False)
    tof = False
    if not len(hrefs) == 0:
        tof = True
    return tof

# URL の画像を表示する
def show_image(url : str, title : str, scaling = 1, ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "show_image", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    try:
        time.sleep(1)
        with requests.get(url, stream = True).raw as resp:
            image = np.asarray(bytearray(resp.read()), dtype = "uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            rescale_size = scaling
            image = cv2.resize(image, dsize = None, fx = rescale_size, fy = rescale_size)
            if ui:
                printer.print("[show] " + url)
            cv2.imshow(title, image)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui:
            printer.print("\x1b[31m" + url + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        # 取得できなかったときは再帰
        show_image(url, title, ui)

# 画像のイメージを PIL.Image で取得
def download_image_for_pil(url, sec = 1, ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "download_image_for_pil", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    # ua_str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    headers = getHeaders()
    try :
        response = requests.get(url, headers = headers)
        # HTTP ステータスコードの確認
        response.raise_for_status()
        if ui:
            printer.print(f"Status Code : {response.status_code}")
        content = response.content
        time.sleep(sec)
    except requests.exceptions.MissingSchema as e:
        if ui:
            printer.print("\x1b[31m")
            printer.print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})")
            printer.print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})", file = sys.stderr)
            printer.print("\x1b[0m")
        return 408, None
    except requests.exceptions.RequestException as e:
        if ui:
            printer.print("\x1b[31m")
            printer.print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})")
            printer.print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})", file = sys.stderr)
            printer.print("\x1b[0m")
        return 408, None
    image_data = io.BytesIO(content)
    try :
        with Image.open(image_data) as im:
            now = datetime.datetime.now()
            tmp_path = f"__{now.year: >4}{now.month:0>2}{now.day:0>2}{now.hour:0>2}{now.minute:0>2}{now.second:0>2}.png"
            # im.save(tmp_path, "PNG")
            # fde.rm(tmp_path, "f", ui = ui)
            im = Image.open(image_data)
            return 0, im
    except UnidentifiedImageError as e:
        if ui:
            printer.print("\x1b[31m")
            printer.print(f"[SoupMaster] 画像の取得に失敗 > Error Code({e}) > URL({url})")
            printer.print(f"[SoupMaster] 画像の取得に失敗 > Error Code({e}) > URL({url})", file = sys.stderr)
            printer.print("\x1b[0m")
        return -1, None

# <a class="anchor_class"> <img src="***"> </a> の *** の部分をリスト化して取り出す
def get_image_urls(soup, anchor_class, ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "get_image_urls", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    anchors = soup.find_all("a", class_ = anchor_class)
    hrefs = []
    for anchor in anchors:
        img = anchor.find('img')
        hrefs.append(str(img['src']))
        if ui:
            printer.print("[append] " + str(img['src']))
    return hrefs

# <tag class="CLASS" id="ID"><img src="***"><img src="***"> ... </tag>
def get_image_urls_in_tag(soup, tag, class_ = None, id_ = None):
    tags = soup.find_all(tag, class_ = class_, id = id_)
    hrefs = []
    for tag in tags:
        imgs = tag.find_all("img")
        for img in imgs:
            hrefs.append(str(img["src"]))
    return hrefs

# <tag class="CLASS"><a href="HREF"><img src="***"></a><a href="HREF"><img src="***"></a></div>
def get_image_urls_in_anchor_in_tag(soup, class_, tag = "div"):
    __srcs = []
    __tags = soup.find_all(tag, class_ = class_)
    for __tag in __tags:
        __anchors = __tag.find_all("a")
        for __anchor in __anchors:
            __imgs = __anchor.find_all("img")
            for __img in __imgs:
                __srcs.append(str(__img["src"]))
    return __srcs

# <tag class="CLASS"><a href="HREF"><img src="***"></a><a href="HREF"><img src="***"></a></div>
def get_image_urls_in_anchor_in_tag_id(soup, id_, tag = "div"):
    __srcs = []
    __tags = soup.find_all(tag, id = id_)
    for __tag in __tags:
        __anchors = __tag.find_all("a")
        for __anchor in __anchors:
            __imgs = __anchor.find_all("img")
            for __img in __imgs:
                __srcs.append(str(__img["src"]))
    return __srcs

def getHeaders():
    headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple WebKit/537.36 (KHTML, like Gecko) Chrome/78.9.3904.97 Safari/537.36",
            "content-type" : "application/json"
            }
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection':
            'keep-alive'
            }
    return headers

# ファイルの種類によらず保存する
def file_download(url, filename, count = 16, ui = False):
    config = {"name" : "SoupMaster", "sub-name" : "file_download", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)
    roop = True
    error = False
    # ヘッダ偽造
    headers = getHeaders()
    while roop:
        try:
            time.sleep(5)
            r = requests.get(url, stream = True, headers = headers)
            roop = False
        except TimeoutError:
            printer.print("[TimeoutError] Retry ... ")
            roop = True
    if not os.path.dirname(filename) == ".":
        fde.mkdir(os.path.dirname(filename))
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    if ui:
        printer.print(f"[Write] {url} -> {filename}")

# 特定のタグ内の要素を取り出す
def get_elements(soup, tag):
    elements = soup.find_all(tag)
    return elements

# URL の画像を cv2 の型で取得
def urlread(url):
    # 画像をリクエスト
    loop = True
    while loop:
        try:
            res = requests.get(url)
            loop = False
        except requests.exceptions.Timeout:
            loop = True
            time.sleep(5)
    img = None
    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(dir = "./") as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img

# <tag class="CLASS"><ul><li>***</li><li>***</li></ul></div>
def get_list_html_to_python(soup, class_ = None, id = None, tag = "div"):
    list_html = []
    div = soup.find(tag, class_ = class_, id = id)
    element_list_htmls = div.find_all("li")
    for element_list_html in element_list_htmls:
        list_html.append(element_list_html.text)
    return list_html

# <tag class = "CLASS"><table><tr><th> KEY </th><td> VAL </td></tr></tag>
def get_dict_html_to_python(soup, class_, tag = "div"):
    dict_html = {}
    div = soup.find(tag, class_ = class_)
    trs = div.find_all("tr")
    for tr in trs:
        th = tr.find("th").text
        td = tr.find("td").text
        dict_html[th] = td

# <TAG1 class = "CLASS" id = "ID"><TAG2 KEY = "VAL"> ... </TAG1>
def get_values_in_tag(soup, tag1, tag2, key, class_ = None, id = None):
    val = []
    tag1s = soup.find_all(tag1, class_ = class_, id = id)
    for tag1 in tag1s:
        tag2s = tag1.find_all(tag2)
        for tag2 in tag2s:
            val.append(tag2[key])
    return val

