import os
import csv
import pickle

INPUTS = [
    "Noun.csv",
    "Noun.org.csv",
    "Noun.verbal.csv"
]
OUTPUT = "vocabulary.pickle"
__dict = dict()  # defaultdict(lambda)をpickleに保存しようとするとエラーになるので普通のdictを使う

with open(os.path.join("data", OUTPUT), "wb") as o:
    for input_file in INPUTS:
        print("input file:", input_file, "-> start")
        with open(os.path.join("data", input_file), "r", encoding="EUC-JP") as i:
            lines = csv.reader(i)
            for line in lines:
                word = line[0]
                yomi = line[-2]
                prefix = yomi[0]
                # とりあえずprefixで登録
                if prefix not in __dict:
                    __dict[prefix] = [word]
                else:
                    __dict[prefix].append(word)
                # 促音 拗音の場合は追加で登録
                if 2 <= len(yomi) and yomi[1] in {"ッ", "ャ", "ュ", "ョ"}:
                    prefix = yomi[:2]
                if prefix not in __dict:
                    __dict[prefix] = [word]
                else:
                    __dict[prefix].append(word)
        print("input file:", input_file, "-> end")
    pickle.dump(__dict, o)
