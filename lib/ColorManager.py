#!/usr/bin/env python3
# coding : utf-8
# 画面上の色を取り出せる

import pyautogui
from pynput import mouse
from PIL import ImageGrab as IG
import numpy as np
import cv2

# data を alpha から beta の間の割合に変換
def data2rate(alpha, beta, data):
    return (data - alpha) / (beta - alpha)

class Coordinate:
    """
    座標を扱えるクラス
    """
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

class Hsv:
    def __init__(self, h_, s_, v_):
        self.h = h_
        self.s = s_
        self.v = v_

class Rgb:
    def __init__(self, r_, g_, b_):
        self.r = r_
        self.g = g_
        self.b = b_

def pil2cv(image):
    new_image = np.array(image, dtype = np.uint8)
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

class ColorManager:
    """
    色や画像を管理するクラス
    """

    def __init__(self, img):
        self.img_ = img
        self.rgbimg_ = img
        self.resizedimg_ = img
        self.convertRGB2HSV()
        self.calcRgbAverage()
        self.convertHSV2RGB()
        self.calcHsvAverage()
        self.calcHex()

    def makeResize(self, f):
        new_image = cv2.resize(self.img_, dsize = None, fx = f, fy = f)
        self.resizedimg_ = new_image

    def makeTrim(self, p1, p2):
        h, w, _ = self.img_.shape[:3]
        p1.x = self.setLimit(p1.x, [0, w])
        p1.y = self.setLimit(p1.y, [0, h])
        p2.x = self.setLimit(p2.x, [0, w])
        p2.y = self.setLimit(p2.y, [0, h])
        self.trimmedimg_ = self.img_[p1.y:p2.y, p1.x:p2.x]

    def setLimit(self, data, limit):
        if limit[1] < limit[0]:
            buf = limit[1]
            limit[1] = limit[0]
            limit[0] = buf
        if data < limit[0]:
            data = limit[0]
        if limit[1] < data:
            data = limit[1]
        return data

    def calcRgbAverage(self, p1 = None, p2 = None):
        image_range = self.rgbimg_
        if (not p1 is None) or (not p2 is None):
            image_range = trim(self.rgbimg_, p1, p2)
        image_range = cv2.cvtColor(image_range, cv2.COLOR_BGR2RGB)
        r = image_range.T[0].flatten().mean()
        g = image_range.T[1].flatten().mean()
        b = image_range.T[2].flatten().mean()
        self.rawrgb_ = Rgb(r, g, b)
        self.ratedrgb_ = Rgb(100 * r / 256, 100 * g / 256, 100 * b / 256)

    def calcHsvAverage(self, p1 = None, p2 = None):
        image_range = self.hsvimg_
        if (not p1 is None) or (not p2 is None):
            image_range = trim(self.hsvimg, p1, p2)
        image_range = cv2.cvtColor(image_range, cv2.COLOR_BGR2HSV)
        h = image_range.T[0].flatten().mean()
        s = image_range.T[1].flatten().mean()
        v = image_range.T[2].flatten().mean()
        self.rawhsv_ = Hsv(h, s, v)
        self.ratedhsv_ = Hsv(360 * h / 256, 100 * s / 256, 100 * v / 256)

    def calcHex(self):
        data = self.rawrgb_
        self.hexedrgb_ = Rgb(hex(round(data.r)), hex(round(data.g)), hex(round(data.b)))
        data = self.rawhsv_
        self.hexedhsv_ = Hsv(hex(round(data.h)), hex(round(data.s)), hex(round(data.v)))

    def convertRGB2HSV(self):
        self.hsvimg_ = cv2.cvtColor(self.img_.astype(np.uint8), cv2.COLOR_RGB2HSV)

    def convertHSV2RGB(self):
        self.rgbimg_ = cv2.cvtColor(self.img_.astype(np.uint8), cv2.COLOR_HSV2RGB)

class ColorPicker:
    """
    ColorPicker class
    画面上の色を取得することが可能
    """
    def __init__(self):
        max_x, max_y = pyautogui.size()
        self.max_ = Coordinate(max_x, max_y)
        with mouse.Listener(on_move = self.onMove, on_click = self.onClick, on_scroll = self.onScroll) as listener:
            listener.join()

    def getPosition(self):
        nowPos = pyautogui.position()
        self.position_ = Coordinate(nowPos[0], nowPos[1])

    def getScreenshot(self):
        short = IG.grab(xdisplay = ":0")
        self.screen_ = pil2cv(short)

    def onMove(self, x, y):
        return

    def onClick(self, x, y, button, pressed):
        self.getPosition()
        self.getScreenshot()
        pos_end_ = Coordinate(self.position_.x + 1, self.position_.y + 1)
        raw_img_ = ColorManager(self.screen_)
        raw_img_.makeTrim(self.position_, pos_end_)
        self.img_ = ColorManager(raw_img_.trimmedimg_)
        rgb = self.img_.hexedrgb_
        print(f"{str(rgb.r)[2:]:0>2}{str(rgb.g)[2:]:0>2}{str(rgb.b)[2:]:0>2}")
        return False

    def onScroll(self, x, y, dx, dy):
        return

class ColorSelector:
    """
    ColorSelector class
    色選択ツールを表示することが可能
    """
    def __init__(self):
        self.tmp = None



