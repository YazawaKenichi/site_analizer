#!/usr/bin/env python3
# coding: utf-8
# FDEditor.py
# ファイル・ディレクトリを操作

import PathEditor as pe
import cv2
import os
import requests

# ファイル名から一行ずつリストに格納
def file2list(filename):
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines

# 画像をコンバートする
def convertor(filepath, ui = True):
    ext = pe.get_ext(filepath)
    if pe.isimage(ext, ui = ui):
        # 画像のときは画像変換
        if ui :
            print("[converting] " + filepath)
        cv2.imwrite(filepath, cv2.imread(filepath))
        if ui :
            print("[converted] " + filepath)
    else:
        # 画像ではないときはスキップ
        if ui :
            print("[skip] " + filepath + " is not image.")

# ディレクトリ内の画像ファイルをコンバートする
def convert_indir(download_dir, ui = True):
    # download_dir 内のファイル名のリストを取得
    image_names = os.listdir(download_dir)
    image_names.sort()
    for image_name in image_names:
        # ファイル名とディレクトリ名からパスを生成
        filepath = download_dir + "/" + image_name
        convertor(filepath, ui = ui)

# ディレクトリ作成
def mkdir(dirname, ui = True):
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError:
            os.makedirs(dirname[0:32])
        if ui:
            print("[mkdir] mkdir -r " + dirname)
    else:
        print("[mkdir] " + dirname + " is already exists.")

# ファイルの中身をまっさらにする
def file_clear(filepath, ui = True):
    with open(filepath, mode="rw") as f:
        f.truncate(0)

