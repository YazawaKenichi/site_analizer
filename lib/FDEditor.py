#!/usr/bin/env python3
# coding: utf-8
# FDEditor.py
# ファイル・ディレクトリを操作

import shutil

import os

# ファイル名から一行ずつリストに格納
def file2list(filename, additional = []):
    r_lines = []
    if os.path.exists(filename):
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

# ディレクトリ名を取得 拡張子が指定されている場合はファイル名を削除
# 指定されていない場合は そのまま返す
def dirname(path):
    _dirname = "./"
    slash = path.rfind("/")
    dot = path.rfind(".")
    if slash < dot:
        _dirname = os.path.dirname(path)
    else:
        _dirname = path
    return str(_dirname)

# ディレクトリ作成
def mkdir(path, ui = False):
    _dirname = dirname(path)
    if not os.path.exists(_dirname):
        try:
            os.makedirs(_dirname)
        except OSError:
            os.makedirs(_dirname[0:32])
        if ui:
            print("[mkdir] mkdir -r " + _dirname)
    else:
        if ui:
            print("[mkdir] " + _dirname + " is already exists.")

# ファイルの中身をまっさらにする
def file_clear(filepath, ui = False):
    with open(filepath, mode="w") as f:
        f.truncate(0)

# 空のファイルを作成する
def touch(filepath, ui = False):
    _dirname = os.path.dirname(filepath)
    if not os.path.isdir(_dirname):
        mkdir(_dirname)
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

# ファイルに文字列を保存 既存のファイルは上書き
def create_file(filepath, text, ui = False):
    if not os.path.exists(filepath):
        touch(filepath)
    with open(filepath, "w") as f:
        f.write(str(text))
        if ui:
            print("[write] " + filepath)
            print(" >>> \r\n" + text, end = "\r\n <<< \r\n")

# ファイル末行に文字列を追加 ファイルがない場合新規作成
def add_file_end(path, text, duplicate = True, ui = False):
    write = True
    # 行の重複が許可されていない場合
    if not duplicate:
        li = file2list(path)
        # 同一の行が存在する場合
        if text in li:
            write = False
    if write:
        with open(path, "a") as f:
            f.write(f"{text}\n")
            if ui:
                print("[write] " + path)
                print(" >>> \r\n" + text, end = "\r\n <<< \r\n")
    return write

# ファイルパスからファイル名（拡張子あり）を取得する
def path2name(filepath, ui = False):
    filename = os.path.basename(filepath)
    return filename

# ディレクトリの削除
def remove(path, trush = "./.trush/"):
    mkdir(trush, ui = False)
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

# ファイルの削除
def rm(path, opt, ui = False):
    yes = "n"
    ret = 0
    if not ("f" in opt):
        yes = input(f"削除しますか？ (yes / no)")
    if ("f" in opt) or (yes.lower()[0] == "y"):
        if ui:
            print(f"削除 : {path}")
        if not "r" in opt:
            os.remove(path)
        else:
            shutil.rmtree(path)
        ret = 0
    else:
        ret = 1
    return ret

# ファイル内に特定の文字列があるかどうか
def check_string_in_file(path, string):
    try:
        with open(path, "r", encoding = "utf-8") as file:
            content = file.read()
            if string in content:
                return True
            else:
                return False
    except FileNotFoundError:
        return False
    except Exception as e:
        return False

