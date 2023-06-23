#!/usr/bin/env python3
# coding: utf-8
# ImageEditor.py
# 画像の操作

import cv2
import shutil
import copy

# 画像をコンバートする
def convertor(src_path, build_path, ui = False):
    if pe.isimage(src_path, ui = ui):
        # 画像のときは画像変換
        if ui :
            print("[converting] " + src_path)
        cv2.imwrite(build_path, cv2.imread(src_path))
        if ui :
            print("[converted] " + build_path)
    else:
        # 画像ではないときはスキップ
        if ui :
            print("[skip] " + src_path + " is not image.")

# 解像度を下げる
def scale_box(src, width, height):
    h, w = src.shape[:2]
    aspect = w / h
    if width / height >= aspect:
        nh = height
        nw = round(nh * aspect)
    else:
        nw = width
        nh = round(nw / aspect)
    dst = cv2.resize(src, dsize = (nw, nh))
    return dst

# HSV 色表現から画像を作成する
def hsv_gen(h, s, v, width = 256, height = 256):
    result = np.full((height, width, 3), (h, s, v))
    image_ = cv2.cvtColor(result.astype(np.float32), cv2.COLOR_HSV2RGB)
    return image_

# RGB 色表現から画像を作成する
def rgb_gen(r, g, b, width = 256, height = 256):
    result = np.full((height, width, 3), (b, g, r))
    return result

# 画像を保存
def writeimage(img, filename = "out.png", ui = False):
    cv2.imwrite(filename, img)

# 画像を表示
def showimage(filepath, window_name = "Lorem Ipsum", ui = False):
    img = cv2.imread(filepath)
    cv2.imshow(window_name, img)
    if ui:
        print("Press any key exit ...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 画像を CLI 表示 fxy には一文字の縦横比を渡す ( 幅 / 高 ) の値
def showimagecli(binary, title = "", fxy = 1 / 3, fullscreen = False, ui = False):
    fx = 1
    fy = fx * fxy
    binary_push = cv2.resize(binary, dsize = None, fx = fx, fy = fy)
    # ターミナルの文字数
    term_size = shutil.get_terminal_size()
    wc_inrow = term_size.columns # 列数
    wc_inline = term_size.lines - 2 # 行数
    small_bin = scale_box(binary_push, wc_inrow, wc_inline)
    if ui:
        binary_original = copy.deepcopy(binary)
        window_name = title
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        if fullscreen:
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, binary_original)
    h, w, _ = small_bin.shape
    image = [["" for i in range(w)] for j in range(h)]
    # 描画
    for y in range(h):
        for x in range(w):
            values = small_bin[y][x]
            b = str(values[0])
            g = str(values[1])
            r = str(values[2])
            print(f"\x1b[48;2;{r};{g};{b}m \x1b[0m", end = "")
        print("\n", end = "")
    # 画像の描画
    """
    for y in range(len(image)):
        for x in range(len(image[0])):
            print(image[y][x], end = "")
        print("\n", end = "")
    """
    return h, w

