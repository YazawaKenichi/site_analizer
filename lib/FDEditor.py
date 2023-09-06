#!/usr/bin/env python3
# coding: utf-8
# FDEditor.py
# ファイル・ディレクトリを操作

SHUTIL = True
try:
    import shutil
except ModuleNotFoundError:
    SHUTIL = False

import os

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

# ディレクトリ内の画像ファイルをコンバートする
def convert_indir(download_dir, ext = ".png", ui = False):
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
def mkdir(dirname, ui = False):
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
def file_clear(filepath, ui = False):
    with open(filepath, mode="w") as f:
        f.truncate(0)

# 空のファイルを作成する
def touch(filepath, ui = False):
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
def create_file(filepath, text, ui = False):
    with open(filepath, "w") as f:
        f.write(str(text))
        if ui:
            print("[write] " + filepath)
            print(" >>> \r\n" + text, end = "\r\n <<< \r\n")

# ファイル末行に文字列を追加
def add_file_end(path, text, ui = False):
    with open(path, "a") as f:
        f.write(f"{text}\n")
        if ui:
            print("[write] " + path)
            print(" >>> \r\n" + text, end = "\r\n <<< \r\n")

# ファイルパスからファイル名（拡張子あり）を取得する
def path2name(filepath, ui = False):
    filename = os.path.basename(filepath)
    return filename

# ディレクトリの削除
def remove(path, trush = "./.trush/"):
    global SHUTIL
    mkdir(trush, ui = False)
    if SHUTIL:
        shutil.move(path, trush)

# ファイルから一致する行を削除
def delinefromfile(path, string):
    tmp_path = "__delinefromfile_template__"
    with open(path, "r") as input:
        with open(tmp_path, "w") as output:
            for line in input:
                if not string in line.strip("\n"):
                    output.write(line)
    os.rename(tmp_path, path)
