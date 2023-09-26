#!/usr/bin/env python3
# coding : utf-8
# LineNotify

import requests

class LINE():
    API_URL = "https://notify-api.line.me/api/notify"

    # コンストラクタ
    def __init__(self, token):
        # ヘッダの設定
        self.__headers = {"Authorization" : f"Bearer {token}"}

    # 送信処理
    def send(self, message, image = None, sticker_package_id = None, sticker_id = None):
        # パラメータ
        payload = {
                "message" : message,
                "stickerPackageId" : sticker_package_id,
                "stickerId" : sticker_id
                }
        files = {}
        # 画像ファイルが指定されている場合は読み込み
        if image != None:
            files = {"imageFile" : open(image, "rb")}
        # 送信
        r = requests.post(LINE.API_URL, headers = self.__headers, data = payload, files = files)

