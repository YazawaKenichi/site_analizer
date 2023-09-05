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

def dir2pdf(src_dir, pdf_path):
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([Image.open(src_dir + j).filename for j in os.listdir(src_dir) if j.endswith(ext)]))

# 画像の URL リストを PDF ファイルに変換
def imgurllist2pdf(urls, path, ui = False):
    imglist_pil = []
    for url in urls:
        if ui :
            print(f"Img URL : {url}")
        # PIL.Image 型の画像を URL から取得
        pil_image = sm.download_image_for_pil(url, ui = False).convert("RGB")
        # PIL.Image をリストに追加する
        imglist_pil.append(pil_image)
    imglist_pil[0].save(path, "PDF", quality = 100, save_all = True, append_images = imglist_pil[1:], optimize = True)

