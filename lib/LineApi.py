#!/usr/bin/env python3
# coding : utf-8
# LineApi

import requests
import urllib.parse
import json
from PrintMaster import Printer

class LINE():
    API_URL = "https://api.line.me/v2/bot/message/broadcast"

    # コンストラクタ
    def __init__(self, token):
        # リクエストヘッダ
        self.__headers = {"Content-Type" : "application/json", "Authorization" : f"Bearer {token}"}

    # 送信処理
    def send(self, message = '', image = None):
        # リクエストボディ
        payload = {"messages" : []}

        if message:
            payload["messages"] = { "type" : "textV2", "text" : message },

        if image:
            _image = urllib.parse.quote(image, safe=':/?=&')
            payload["messages"] = { "type" : "image", "originalContentUrl" : _image, "previewImageUrl" : _image },

        print(payload)

        # 送信
        r = requests.post(LINE.API_URL, headers = self.__headers, json = payload)

        return r

