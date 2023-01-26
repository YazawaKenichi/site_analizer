#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier:

import SoupMaster as sm
import sys
from optparse import OptionParser

# 引数を解析する
def get_args(ui = True):
    usage = "Usage: %prog"
    parser = OptionParser(usage = usage)

    # -s オプションで表示画像のサイズを指定できるようにする
    parser.add_option(
            "-s", "--scaling",
            default = "0.4",
            type = "float",
            dest = "scalingsize",
            help = "表示画像のサイズを入力\r\nデフォルトで 0.4"
            )

    parser.add_option(
            "-o", "--output",
            default = "./a.html",
            type = "string",
            dest = "output",
            help = "出力ファイル名"
            )

    if ui:
        optdict, args = parser.parse_args()
        print("[args] ", optdict, args)
    return parser.parse_args()

if __name__ == "__main__":
    UI = True
    optiondict, args = get_args()
    if len(args) == 0:
        print("[Error] URL が指定されていません", file = sys.stderr)
        sys.exit(1)
    print(optiondict)
    filename = optiondict.output
    url = args[0]
    try:
        sm.file_download(url, filename, UI)
    except:
        print("[Error] 404 Page Not Found", file = sys.stderr)
        sys.exit(1)
    print("End of Program")
    sys.exit(0)

