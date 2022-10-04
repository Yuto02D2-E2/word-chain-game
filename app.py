import os
import pickle
import MeCab
import random
import functools


class Game:
    def __init__(self) -> None:
        try:
            with open(os.path.join("data", "vocabulary.pickle"), "rb") as f:
                self.__dict = pickle.load(f)
        except Exception:
            self.__dict = {
                "ア": ["雨", "蟻", "朝顔"],
                "イ": ["椅子"],
                "ウ": ["嘘"],
                "エ": ["エラトステネスの篩"],
                "オ": ["お餅"],
                "コ": ["こぶた"],
                "タ": ["たぬき"],
                "キ": ["きつね"],
                "ネ": ["ねこ"]
            }
        self.__used_word = set()
        return

    @functools.lru_cache(maxsize=512)
    def get_yomi(self, word: str) -> str:
        # 単語の"読み"を返す(全角カタカナ)
        return MeCab.Tagger("-O yomi").parse(word).strip()

    @functools.lru_cache(maxsize=512)
    def get_prefix(self, word: str) -> str:
        yomi = self.get_yomi(word)
        if 2 <= len(yomi) and yomi[1] in {"ッ", "ャ", "ュ", "ョ"}:
            return yomi[:2]
        else:
            return yomi[0]

    @functools.lru_cache(maxsize=512)
    def get_suffix(self, word: str) -> str:
        yomi = self.get_yomi(word)
        if 2 <= len(yomi) and yomi[-1] in {"ッ", "ャ", "ュ", "ョ"}:
            return yomi[-2:]
        else:
            return yomi[-1]

    def get_cpu_word(self, user_word: str) -> str:
        user_word_suffix = self.get_suffix(user_word)
        if user_word_suffix in self.__dict:
            return random.choice(self.__dict[user_word_suffix])
        return None

    def check_word_end(self, word: str, player: str) -> bool:
        if self.get_suffix(word) == "ン":
            print(f"> 'ん'で終わっています．{player}の負けです．")
            return False
        return True

    def check_history(self, word: str, player: str) -> bool:
        if self.get_yomi(word) in self.__used_word:
            print(f"> 同じ単語を二度以上使うことは出来ません．{player}の負けです．")
            return False
        self.__used_word.add(self.get_yomi(word))
        return True

    def check_connect(self, prev_word: str, cur_word: str, cur_player: str) -> bool:
        if self.get_suffix(prev_word) != self.get_prefix(cur_word):
            print(f"> 前の言葉と繋がっていません．{cur_player}の負けです．")
            return False
        return True

    def main(self) -> None:
        init = True  # 最初の一手は繫がり判定をしないためのフラグ
        print("")
        print("しりとりゲーム")
        print("- 入力は全角ひらがな，全角カタカナ，全角漢字を受け付けます")
        print("- 先攻はユーザーです")
        print("")
        while True:
            # User
            user_word = input("user:")
            if not self.check_word_end(user_word, "user"):
                return
            if not self.check_history(user_word, "user"):
                return
            if init:
                cpu_word = self.get_prefix(user_word)
                init = False
            if not self.check_connect(cpu_word, user_word, "user"):
                return

            # CPU
            cpu_word = self.get_cpu_word(user_word)
            if cpu_word is None:
                print("> 思いつきません．cpuの負けです...")
                return
            print(f"cpu:{cpu_word}({self.get_yomi(cpu_word)})")
            if not self.check_word_end(cpu_word, "cpu"):
                return
            if not self.check_history(cpu_word, "cpu"):
                return
            if not self.check_connect(user_word, cpu_word, "cpu"):
                return


if __name__ == '__main__':
    Game().main()
