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
        pil_image_raw = sm.download_image_for_pil(url, sec = sec, ui = ui)
        if not pil_image_raw == -1:
            pil_image = pil_image_raw.convert("RGB")
            # PIL.Image をリストに追加する
            imglist_pil.append(pil_image)
    if len(imglist_pil) > 0:
        imglist_pil[0].save(path, "PDF", quality = 100, save_all = True, append_images = imglist_pil[1:], optimize = True)
        ret = 0
    else:
        ret = -1
    return ret

