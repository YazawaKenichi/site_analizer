#!/usr/bin/env python3
# coding : utf-8

import requests
from optparse import OptionParser
from LineNotify import LINE

def get_args(ui = False):
    usage = "%prog ACCESS_TOKEN [-v]"
    parser = OptionParser(usage = usage)

    parser.add_option(
            "-v",
            action = "store_true",
            default = False,
            dest = "visible",
            help = "デバッグモード"
            )

    parser.add_option(
            "-m",
            type = "string",
            default = None,
            dest = "media",
            help = "メディア"
            )

    return parser.parse_args()

if __name__ == "__main__":
    optiondict, args = get_args(ui = False)
    media = optiondict.media
    ui = optiondict.visible

    # 送信先 URL
    access_token = args[0]
    # メッセージ
    message = "".join(args[1:])
    # インスタンス化
    line = LINE(token = access_token)

    # 送信
    line.send(message = message, image = media, sticker_package_id = None, sticker_id = None)



