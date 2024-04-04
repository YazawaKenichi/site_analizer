#!/usr/bin/env python3
# coding : utf-8
# GamePlayer.py
import GUIMaster
import cv2

class FindTemplate:
    def __init__(self, template):
        self.setTemplate(template)
    def setTemplate(self, template):
        self.template = template
    def findTemplate(self, game_screen):
        # game_screen 内にTemplate が存在するか
        # result は類似性マップ
        result = cv2.matchTemplate(game_screen, self.template, cv2.TM_CCOEFF_NORMED)
        # テンプレート画像の位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # Calculate player icon position
        try:
            h, w, _ = self.template.shape
        except ValueError:
            h, w = self.template.shape
        x = max_loc[0] + w // 2
        y = max_loc[1] + h // 2
        return x, y

if __name__ == "__main__":
    path = "test.png"
    player = cv2.imread(path)
    screenshot = GUIMaster.getScreenshot()
    finder = FindTemplate(player)
    x, y = finder.findTemplate(screenshot)
    print(f"Player Position : ({x:4>}, {y:4>})")

