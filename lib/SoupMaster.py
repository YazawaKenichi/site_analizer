#!/usr/bin/env python3
# coding: utf-8
# SoupMaster.py
# HTML を操作

import time
import urllib
from urllib import request
import chardet
from bs4 import BeautifulSoup
import requests
import sys

# アドレスの BeautifulSoup を返す
def get_soup(address, ui = True):
    try:
        # ユーザエージェントの偽装
        headers = {"User-Agent" : "camouflage useragent"}
        req = request.Request(url = address, headers = headers)
        # レスポンスの情報を管理するオブジェクトを返す
        # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
        with request.urlopen(req) as response:
            time.sleep(0.5)
            # 取得した文字列をまとめて取り出す
            body = response.read()
            if ui:
                print("[open] " + address)
            try:
                # 文字コードの取得
                cs = chardet.detect(body)   # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
                data = body.decode(cs['encoding'])
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'html.parser')
                return soup
            except UnicodeDecodeError:
                data = body
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'html.parser')
                return soup
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        get_soup(address, ui)

# 特定クラス名を持つタグの要素を取得
def get_tags_from_class(soup, class_, tag = "div", ui = True):
    lists = soup.find_all(tag, class_ = class_)
    return lists

# 特定の ID 名を持つタグの要素を取得
def get_tags_from_id(soup, id, tag = "div", ui = True):
    lists = soup.find_all(tag, id = id)
    return lists

# <a class = anchor_class href = "***" ></a>
def get_hrefs(soup, anchor_class, ui = True):
    lists = soup.find_all(class_ = anchor_class)
    hrefs = []
    for li in lists:
        hrefs.append(str(li['href']))
        if ui:
            print("[append] " + str(li['href']))
    return hrefs

# <tag class = tag_class><a href = "***"></a></tag>
def get_hrefs_from_tag_in_anchor(soup, tag_class, tag = "div", ui = True):
    # tag_class を持つ tag のリストを取得する
    lists = get_tags_from_class(soup, class_ = tag_class, tag = tag, ui = ui)
    if ui:
        print("[get] ", lists)
    return lists

# bs4.BeautifulSoup 型にして返す
def elementTag2BeautifulSoup(data, ui = True):
    string = ""
    string = str(data)
    soup = BeautifulSoup(string, 'lxml')
    return soup

# href があるかどうかを判断する
def exist_href(soup, anchor_class, ui = True):
    hrefs = get_hrefs(soup, anchor_class, ui = False)
    tof = False
    if not len(hrefs) == 0:
        tof = True
    return tof

# URL の画像を表示する
def show_image(url : str, title : str, scaling = 1, ui = True):
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

# <a class="anchor_class"> <img src="***"> </a> の *** の部分をリスト化して取り出す
def get_image_urls(soup, anchor_class, ui = True):
    anchors = soup.find_all(class_ = anchor_class)
    hrefs = []
    for anchor in anchors:
        img = anchor.find('img')
        hrefs.append(str(img['src']))
        if ui:
            print("[append] " + str(img['src']))
    return hrefs

# ファイルの種類によらず保存する
def file_download(url, filename, ui = True):
    roop = True
    # ヘッダ偽造
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple WebKit/537.36 (KHTML, like Gecko) Chrome/78.9.3904.97 Safari/537.36"}
    while roop:
        try:
            time.sleep(5)
            r = requests.get(url, stream = True, headers = headers)
            roop = False
        except TimeoutError:
            file_download(url, filename, ui)
            print("[TimeoutError] Retry ... ")
            roop = True
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    if ui :
        print("[write] " + url + " -> " + filename)

