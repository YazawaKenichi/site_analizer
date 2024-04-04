#!/usr/bin/env python3
import pyautogui
import cv2
import numpy as np
import copy

def showImage(txt, img, ui = True):
    if ui:
        cv2.imshow(f"{txt}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def getScreenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def drawPoint(_image, p, c = (0, 0, 255), t = 2, ui = False):
    x = p[0]
    y = p[1]
    image = copy.deepcopy(_image)
    cv2.circle(image, (x, y), t, c, -1)
    if ui:
        txt = f"GUIMaster.drawPoint({x}, {y})"
        showImage(txt, image, ui = ui)
    return image

def drawCircle(_image, p = (0, 0), r = 10, c = (0, 0, 255), t = 2, ui = False):
    image = copy.deepcopy(_image)
    cv2.circle(image, p, r, c, t)
    if ui:
        txt = f"GUIMaster.drawCircle({x}, {y})"
        showImage(txt, image, ui = ui)
    return image

def drawCrosshair(_image, p = (0, 0), r = 10, c = (0, 0, 255), t = 2, ui = False):
    x = p[0]
    y = p[1]
    image = copy.deepcopy(_image)
    image = drawCircle(image, (x, y), r = r, c = c, t = t)
    u = (x, int(y - r * 1.5))
    d = (x, int(y + r * 1.5))
    l = (int(x - r * 1.5), y)
    r = (int(x + r * 1.5), y)
    image = cv2.line(image, u, d, c, t)
    image = cv2.line(image, l, r, c, t)
    if ui:
        txt = f"GUIMaster.drawCrosshair({x}, {y})"
        showImage(txt, image, ui = ui)
    return image

def moveTo(x, y):
    pyautogui.moveTo(x, y)

def dragTo(x, y, d):
    pyautogui.dragTo(x, y, duration = d)

