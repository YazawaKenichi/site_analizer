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
from tqdm import tqdm
from PrintMaster import Printer

def dir2pdf(src_dir, pdf_path):
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([Image.open(src_dir + j).filename for j in os.listdir(src_dir) if j.endswith(ext)]))

# 画像の URL リストを PDF ファイルに変換
def imgurllist2pdf(urls, path, sec = 1, ui = False):
    ret = 0
    imglist_pil = []

    config = {"name" : "PDFEditor", "sub-name" : "imgurllist2pdf", "screen-full" : True}
    printer = Printer()
    printer.addConfig(config)

    for url in tqdm(urls, desc = "Convert"):
        if ui :
            printer.print(f"Img URL : {url}")
        # PIL.Image 型の画像を URL から取得
        able, pil_image_raw = sm.download_image_for_pil(url, sec = sec, ui = ui)
        if able == 404 or able == 408:
            printer.print("\x1b[31m")
            printer.print(f"[PDFEditor] {able} HTTP Error")
            printer.print(f"[PDFEditor] {able} HTTP Error", file = sys.stderr)
            printer.print("\x1b[0m")
        elif able == -1:
            if pe.isimage(url, ui = ui):
                printer.print("\x1b[31m")
                printer.print(f"[PDFEditor] {url} is not image.")
                printer.print(f"[PDFEditor] {url} is not image.", file = sys.stderr)
                printer.print("\x1b[0m")
            else:
                printer.print("\x1b[31m")
                printer.print(f"[PDFEditor] {url} is image but unexcepted error.")
                printer.print(f"[PDFEditor] {url} is image but unexcepted error.", file = sys.stderr)
                printer.print("\x1b[0m")
        else:
            pil_image = pil_image_raw.convert("RGBA")
            # PIL.Image をリストに追加する
            imglist_pil.append(pil_image)
        if ret == 0:
            ret = able
    if len(imglist_pil) > 0:
        imglist_pil[0].save(path, "PDF", quality = 100, save_all = True, append_images = imglist_pil[1:], optimize = True)
    return ret

