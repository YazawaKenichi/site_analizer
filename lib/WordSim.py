#!/usr/bin/env python3

import re
import sys
import phonetics
from gensim.models import KeyedVectors
from scipy.spatial.distance import euclidean, cosine
import fuzzy
import gensim.downloader as api
from janome.tokenizer import Tokenizer, Token

# 類似度を格納する構造体
class Similarity:
    def __init__(self, a = "", b = "", d = 0.0, text = ""):
        self.distance = d
        self.words = [a, b]
        self.text = text

# レーベンシュタイン距離
class LevenshteinDistance:
    def __init__(self):
        self.res = Similarity()
    def distance(self, s1, s2):
        m, n = len(s1), len(s2)
        # Create a matrix to hold the distances
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        # Initialize the first row and column of the matrix
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        # Compute the distances
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                                   dp[i][j - 1] + 1,  # Insertion
                                   dp[i - 1][j - 1] + 1)  # Substitution
        return dp[m][n]
    def similarity(self, distance):
        ret = ""
        if distance == 0:
            ret = "完全に一致"
        elif distance <= 2:
            ret = "わりと似てる"
        elif distance <= 4:
            ret = "なんとも言えない"
        else :
            ret = "全然違う"
        return ret
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

# ユークリッド距離
class EuclideanDistance:
    def __init__(self, model):
        self.res = Similarity()
        self.model = None
        self.model = KeyedVectors.load_word2vec_format(model, binary = True)
        self.model = api.load(model)
    def distance(self, a, b):
        distance = None
        if not self.model is None:
            v1 = self.model[a]
            v2 = self.model[b]
            distance = euclidean(v1, v2)
        return distance
    def similarity(self, distance):
        return "開発中"
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

# ジャッカード類似度
class JaccardSimilarity:
    def __init__(self):
        self.res = Similarity()
    def distance(self, a, b):
        s1 = set(a)
        s2 = set(b)
        intersection = len(s1.intersection(s2))
        union = len(s1.union(s2))
        ret = 0
        if union == 0:
            ret = 0
        else:
            ret = intersection / union
        return ret
    def similarity(self, distance):
        ret = ""
        if distance == 1.0:
            ret = "完全に一致"
        elif distance >= 0.7:
            ret = "わりと似てる"
        elif distance >= 0.4:
            ret = "なんとも言えない"
        elif distance >= 0.1:
            ret = "だいぶ違う"
        else:
            ret = "全然違う"
        return ret
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

# Word Mover's Distance (WMD)
class WordMoversDistance:
    def __init__(self, model = "word2vec-google-news-300"):
        self.res = Similarity()
        self.model = api.load(model)
    def preprocess(self, text):
        return text.split()
    def distance(self, a, b):
        que = self.preprocess(a)
        ref = self.preprocess(b)
        sentences = [que, ref]
        wmd_sim = WmdSimilarity(sentences, self.model)
        ret = wmd_sim[que, ref]
        return ret
    def similarity(self, distance):
        return "開発中"
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

# フォネティック類似度 ( 開発中 ）
class PhoneticSimilarity:
    def __init__(self):
        self.res = Similarity()
    def distance(self, a, b):
        ret = None
        try:
            soundex = fuzzy.Soundex(4)
            ret = soundex(a) == soundex(b)
        except:
            tokenizer = Tokenizer()
            t1 = [token.surface for token in tokenizer.tokenize(a)]
            t2 = [token.surface for token in tokenizer.tokenize(b)]
            ret = (t1 == t2)
        return ret
    def similarity(self, distance):
        return "一緒" if distance else "違う"
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

# N 音節一致
class NSyllableSimilarity:
    def __init__(self):
        self.res = Similarity()
    def count_syllables(self, w):
        w = w.lower()
        w = re.sub(r"[aeiouy]+", "a", w)
        syllables = len(re.findall(r"[aeiouy]", w))
        return syllables
    def distance(self, a, b):
        s1 = self.count_syllables(a)
        s2 = self.count_syllables(b)
        _min = min(s1, s2)
        _max = max(s1, s2)
        ret = None
        if not _max == 0:
            ret = _min / _max
        return ret
    def similarity(self, distance):
        return "開発中"
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

# コサイン類似度
class CosineSimilarity:
    def __init__(self, model = "word2vec-google-news-300"):
        self.res = Similarity()
        self.model = api.load(model)
    def distance(self, a, b):
        v1 = self.model[a]
        v2 = self.model[b]
        ret = 1 - cosine(v1, v2)
        return ret
    def similarity(self, distance):
        return "開発中"
    def result(self, a, b):
        d = self.distance(a, b)
        t = self.similarity(d)
        self.res = Similarity(a, b, d, t)
        return self.res

if __name__ == "__main__":
    import argparse
    import os

    def getArgs():
        parser = argparse.ArgumentParser()
        parser.add_argument("que",
                action = "store",
                default = None,
                # dest = "que",
                help = "比較対象",
                metavar = "QUE",
                # required = True,
                type = str,
                )
        parser.add_argument("ref",
                action = "store",
                default = None,
                # dest = "ref",
                help = "比較対象",
                metavar = "REF",
                # required = True,
                type = str,
                )
        parser.add_argument("-m", "--model",
                action = "store",
                default = "./w2v/ja/ja.bin",
                dest = "model",
                help = "Word to Vector Model Binaly File PATH",
                metavar = "MODEL_PATH",
                required = False,
                type = str,
                )
        return parser.parse_args()

    def isAscii(s):
        return all(ord(c) < 128 for c in s)

    args = getArgs()

    s1 = args.que
    s2 = args.ref

    model = args.model

    # レーベンシュタイン距離
    ld = LevenshteinDistance()
    res = ld.result(s1, s2)
    print(f"レーベンシュタイン距離 : {res.distance} > {res.text}")

    if os.path.exists(model):
        # ユークリッド距離
        ld = EuclideanDistance(model)
        res = ld.result(s1, s2)
        print(f"ユークリッド距離 : {res.distance} > {res.text}")

    # ジャッカード類似度
    ld = JaccardSimilarity()
    res = ld.result(s1, s2)
    print(f"ジャッカード類似度 : {res.distance} > {res.text}")

    if os.path.exists(model):
        # Word Mover's Distance
        ld = WordMoversDistance(model)
        res = ld.result(s1, s2)
        print(f"Word Mover's Distance ( WMD ) : {res.distance} > {res.text}")

    # フォネティック類似度
    ld = PhoneticSimilarity()
    res = ld.result(s1, s2)
    print(f"フォネティック類似度 : {res.distance} > {res.text}")

    if isAscii(s1) and isAscii(s2):
        # N 音節一致
        ld = NSyllableSimilarity()
        res = ld.result(s1, s2)
        print(f"N 音節一致 : {res.distance} > {res.text}")

    if os.path.exists(model):
        # コサイン類似度
        ld = CosineSimilarity(model)
        res = ld.result(s1, s2)
        print(f"コサイン類似度 : {res.distance} > {res.text}")

