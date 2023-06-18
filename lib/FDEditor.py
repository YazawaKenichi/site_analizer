#!/usr/bin/env python3
# coding: utf-8
# FDEditor.py
# ファイル・ディレクトリを操作

import PathEditor as pe
CV2 = True
try:
    import cv2
except ModuleNotFoundError:
    CV2 = False
import os
import requests

# ファイル名から一行ずつリストに格納
def file2list(filename, additional = []):
    with open(filename) as f:
        lines = []
        for line in f:
            line = line.replace("\n", "")
            line = line.replace(" ", "")
            line = line.split("#")[0]
            if not line == "":
                lines.append(line)
    r_lines = list(dict.fromkeys(lines))
    if not additional is None:
        r_lines = additional + r_lines
    return r_lines

# 画像をコンバートする
def convertor(src_path, build_path, ui = True):
    global CV2
    if pe.isimage(src_path, ui = ui):
        # 画像のときは画像変換
        if ui :
            print("[converting] " + src_path)
        if CV2:
            cv2.imwrite(build_path, cv2.imread(src_path))
        if ui :
            print("[converted] " + build_path)
    else:
        # 画像ではないときはスキップ
        if ui :
            print("[skip] " + src_path + " is not image.")

# ディレクトリ内の画像ファイルをコンバートする
def convert_indir(download_dir, ext = ".png", ui = True):
    # download_dir 内のファイル名のリストを取得
    image_names = os.listdir(download_dir)
    image_names.sort()
    for image_name in image_names:
        image_name_split = os.path.splitext(os.path.basename(image_name))[0]
        # ファイル名とディレクトリ名からパスを生成
        src = download_dir + image_name
        build = download_dir + image_name_split + ext
        convertor(src, build, ui = ui)

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
        if ui:
            print("[mkdir] " + dirname + " is already exists.")

# ファイルの中身をまっさらにする
def file_clear(filepath, ui = True):
    with open(filepath, mode="w") as f:
        f.truncate(0)

# 空のファイルを作成する
def touch(filepath, ui = True):
    if not os.path.exists(filepath):
        with open(filepath, mode = "w") as f:
            f.truncate(0)
    else:
        if ui:
            print("[touch] " + str(filepath) + " is already exists.")

# ディレクトリ内のディレクトリやファイルの拡張子あり名前を取得する
def get_listdir(dir_path):
    ld = os.listdir(dir_path)
    ld.sort()
    return ld

# ファイルに文字列を保存
def create_file(filepath, text, ui = True):
    with open(filepath, "w") as f:
        f.write(str(text))
        if ui:
            print("[write] " + filepath)
            print(" >>> \r\n" + text, end = "\r\n <<< \r\n")

# ファイルパスからファイル名（拡張子あり）を取得する
def path2name(filepath, ui = True):
    filename = os.path.basename(filepath)
    return filename

# ファイルから一致する行を削除
def delinefromfile(path, string):
    tmp_path = "__delinefromfile_template__"
    with open(path, "r") as input:
        with open(tmp_path, "w") as output:
            for line in input:
                if not string in line.strip("\n"):
                    output.write(line)
    os.rename(tmp_path, path)
