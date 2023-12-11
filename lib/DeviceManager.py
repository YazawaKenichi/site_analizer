#!/usr/bin/env python3
# coding : utf-8

from PIL import ImageGrab as IG
import ImageEditor as ie

def screenshot(p1, p2):
    shot = IG.grab()
    cv_shot = ie.pil2cv(shot)
    return ie.trim(cv_shot, p1, p2)

