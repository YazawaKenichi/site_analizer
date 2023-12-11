#!/usr/bin/env python3
# coding : utf-8
# Standard Library

# raw の値を low <= raw <= high に収める
def limit(raw, low, high):
    # low のほうが高かったら high と low を入れ替える
    if high < low:
        buf = high
        high = low
        low = buf
    # low よりも小さかったら low にする
    if raw < low:
        raw = low
    # high よりも大きかったら high にする
    if high < raw:
        raw = high
    return raw

def extend(_a, _b):
    for __b in _b:
        _a.append(__b)
    return _a

