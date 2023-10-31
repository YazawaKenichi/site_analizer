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

# アドレスの BeautifulSoup を返す
def get_soup(address, ui = False):
    try:
        # ユーザエージェントの偽装
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = { "User-Agent" : user_agent }
        # レスポンスの情報を管理するオブジェクトを返す
        # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
        with requests.get(address, headers = header) as response:
            time.sleep(0.5)
            # 取得した文字列をまとめて取り出す
            body = response.content
            data = body
            if ui:
                print("[open] " + address)
            soup = BeautifulSoup(data, "html.parser")
            return soup
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        get_soup(address, ui)

def print_element(elem):
    if isinstance(elem, bs4.NavigableString):
        print(type(elem), elem.string)
    else:
        print(type(elem), elem.name)

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
    lists = soup.find_all(class_ = anchor_class)
    hrefs = []
    for li in lists:
        hrefs.append(str(li['href']))
        if ui:
            print("[append] " + str(li['href']))
    return hrefs

# <tag class = tag_class><a href = "***"></a></tag>
def get_hrefs_from_tag_in_anchor(soup, class_, tag = "div", recursion = True, ui = False):
    # tag_class を持つ tag のリストを取得する
    lists = get_tags_from_class(soup, class_ = class_, tag = tag, ui = ui)
    hrefs = []
    for li in lists:
        anchors = []
        anchors = li.find_all("a")
        for anchor in anchors:
            hrefs.append(str(anchor['href']))
    if ui:
        print("[get] ", lists)
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
    try:
        time.sleep(1)
        with requests.get(url, stream = True).raw as resp:
            image = np.asarray(bytearray(resp.read()), dtype = "uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            rescale_size = scaling
            image = cv2.resize(image, dsize = None, fx = rescale_size, fy = rescale_size)
            if ui:
                print("[show] " + url)
            cv2.imshow(title, image)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui:
            print("\x1b[31m" + url + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        # 取得できなかったときは再帰
        show_image(url, title, ui)

# 画像のイメージを PIL.Image で取得
def download_image_for_pil(url, sec = 1, ui = False):
    # ua_str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    ua_str = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1"
    headers = {
        'User-Agent': ua_str,
        'content-type': 'application/json'
    }
    try :
        response = requests.get(url, headers = headers)
        # HTTP ステータスコードの確認
        response.raise_for_status()
        if ui:
            print(f"Status Code : {response.status_code}")
        content = response.content
        time.sleep(sec)
    except requests.exceptions.MissingSchema as e:
        if ui:
            print("\x1b[31m")
            print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})")
            print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})", file = sys.stderr)
            print("\x1b[0m")
        return 408, None
    except requests.exceptions.RequestException as e:
        if ui:
            print("\x1b[31m")
            print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})")
            print(f"[SoupMaster] リクエストが返されませんでした > Error Code({e}) > URL({url})", file = sys.stderr)
            print("\x1b[0m")
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
            print("\x1b[31m")
            print(f"[SoupMaster] 画像の取得に失敗 > Error Code({e}) > URL({url})")
            print(f"[SoupMaster] 画像の取得に失敗 > Error Code({e}) > URL({url})", file = sys.stderr)
            print("\x1b[0m")
        return -1, None

# <a class="anchor_class"> <img src="***"> </a> の *** の部分をリスト化して取り出す
def get_image_urls(soup, anchor_class, ui = False):
    anchors = soup.find_all(class_ = anchor_class)
    hrefs = []
    for anchor in anchors:
        img = anchor.find('img')
        hrefs.append(str(img['src']))
        if ui:
            print("[append] " + str(img['src']))
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

# ファイルの種類によらず保存する
def file_download(url, filename, ui = False):
    roop = True
    # ヘッダ偽造
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple WebKit/537.36 (KHTML, like Gecko) Chrome/78.9.3904.97 Safari/537.36"}
    while roop:
        try:
            time.sleep(5)
            r = requests.get(url, stream = True, headers = headers)
            roop = False
        except TimeoutError:
            print("[TimeoutError] Retry ... ")
            roop = True
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    if ui:
        print(f"[Write] {url} -> {filename}")

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

