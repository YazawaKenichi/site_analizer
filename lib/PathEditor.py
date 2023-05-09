#!/usr/bin/env python3
# coding: utf-8
# PathEditor.py
# 文字列を操作

import os

NAMELENGTH = 64

# ファイル名拡張子なしを取り出す
def get_basename(path, ui = False):
    res = ""
    dot_index = path.find(".")
    if not dot_index == 0:
        res = os.path.basename(path)[0]
    else:
        res = ""
    if ui:
        print("[basename] ", os.path.basename(path))
    return str(res)

# 拡張子を取り出す
def get_ext(path, ui = False):
    res = ""
    dot_index = path.find(".")
    res = os.path.splitext(path)[-1]
    if ui:
        print("[splitext] ", os.path.splitext(path))
    return str(res)

# 文字列から接頭辞を削除する
def cut_prefix(string, prefix, ui = True):
    res = string[len(prefix) :]
    return res

# スラッシュをパイプに変えて長い文字列を短くする
def path_short(path, namelength = NAMELENGTH, ui = True):
    ext = get_ext(path, ui = False)
    # スラッシュをパイプに置き換える
    path_opt = path.replace("/", "|")
    namelength_ = namelength - len(ext)
    # ファイル名が長くなったときに短くする
    if len(path_opt) >= namelength_:
        path_opt = path_opt[:namelength_]
        path_opt = path_opt + ext
    return path_opt

# 指定文字列が画像を示すかどうかを返す
def isimage(path, ui = True):
    imageexies = [".jpg", ".jpeg", ".png", ".ping", ".webp", ".jfif", ".svg"]
    ext = get_ext(path, ui = False)
    if ui:
        msg = f"[compare] path : {path} | ext : {ext} | {ext in imageexies}"
        print(msg)
    return ext in imageexies

