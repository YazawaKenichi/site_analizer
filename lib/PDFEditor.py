#!/usr/bin/env python3
# coding : utf-8
# PDFEditor.py

import os
import img2pdf
from PIL import Image
import cv2
import shutil
import sys
import SoupMaster as sm
import PathEditor as pe
import time

def dir2pdf(src_dir, pdf_path):
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([Image.open(src_dir + j).filename for j in os.listdir(src_dir) if j.endswith(ext)]))

# 画像の URL リストを PDF ファイルに変換
def imgurllist2pdf(urls, path, sec = 1, ui = False):
    ret = 0
    imglist_pil = []
    for url in urls:
        if ui :
            print(f"Img URL : {url}")
        # PIL.Image 型の画像を URL から取得
        able, pil_image_raw = sm.download_image_for_pil(url, sec = sec, ui = ui)
        if able == 404 or able == 408:
            print("\x1b[31m")
            print(f"[PDFEditor] {ret} HTTP Error")
            print(f"[PDFEditor] {ret} HTTP Error", file = sys.stderr)
            print("\x1b[0m")
        elif able == -1:
            if pe.isimage(url, ui = ui):
                print("\x1b[31m")
                print(f"[PDFEditor] {url} is not image.")
                print(f"[PDFEditor] {url} is not image.", file = sys.stderr)
                print("\x1b[0m")
            else:
                print("\x1b[31m")
                print(f"[PDFEditor] {url} is image but unexcepted error.")
                print(f"[PDFEditor] {url} is image but unexcepted error.", file = sys.stderr)
                print("\x1b[0m")
        else:
            pil_image = pil_image_raw.convert("RGBA")
            # PIL.Image をリストに追加する
        if ret == 0:
            ret = able
            imglist_pil.append(pil_image)
    if len(imglist_pil) > 0:
        imglist_pil[0].save(path, "PDF", quality = 100, save_all = True, append_images = imglist_pil[1:], optimize = True)
    return ret

