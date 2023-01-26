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

# アドレスの BeautifulSoup を返す
def get_soup(address, ui = True):
    try:
        # レスポンスの情報を管理するオブジェクトを返す
        # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
        with request.urlopen(address) as response:
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
                soup = BeautifulSoup(data, 'lxml')
                return soup
            except UnicodeDecodeError:
                data = body
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'lxml')
                return soup
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        get_soup(address, ui)

# 特定クラス名を持つ div タグの要素を取得
def get_divs(soup, div_class, ui = True):
    lists = soup.find_all(class_ = div_class)
    return lists

# 特定のクラス名を持つ anchor タグの href 属性内容を取得
def get_hrefs(soup, anchor_class, ui = True):
    lists = soup.find_all(class_ = anchor_class)
    hrefs = []
    for li in lists:
        hrefs.append(str(li['href']))
        if ui:
            print("[append] " + str(li['href']))
    return hrefs

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
        with requests.get(url, stream = True).raw as resp:
            time.sleep(0.5)
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
    r = requests.get(url, stream = True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    if ui :
        print("[write] " + url + " -> " + filename)

