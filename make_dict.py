import os
import csv
import pickle

INPUTS = [
    "Noun.csv",
    "Noun.org.csv",
    "Noun.verbal.csv"
]
OUTPUT = "vocabulary.pickle"
_dict = dict()  # defaultdict(lambda)をpickleに保存しようとするとエラーになるので普通のdictを使う

with open(os.path.join("data", OUTPUT), "wb") as o:
    for input_file in INPUTS:
        print("input file:", input_file, "-> start")
        with open(os.path.join("data", input_file), "r", encoding="EUC-JP") as i:
            lines = csv.reader(i)
            for line in lines:
                word, prefix = line[0], line[-2][0]
                if prefix not in _dict:
                    _dict[prefix] = [word]
                else:
                    _dict[prefix].append(word)
        print("input file:", input_file, "-> end")
    pickle.dump(_dict, o)
