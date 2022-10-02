import os
import pickle
import MeCab
import random
import functools


try:
    with open(os.path.join("data", "vocabulary.pickle"), "rb") as f:
        _dict = pickle.load(f)
except Exception:
    _dict = {
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
used_word = set()


@functools.lru_cache(maxsize=512)
def get_yomi(word: str) -> str:
    # 単語の"読み"を返す(全角カタカナ)
    return MeCab.Tagger("-O yomi").parse(word).strip()


def get_cpu_word(user_word: str) -> str:
    last_char = get_yomi(user_word)[-1]
    if last_char not in _dict:
        return None
    return random.choice(_dict[last_char])


def check_history(word: str, player: str) -> bool:
    if get_yomi(word) in used_word:
        print(f"> 同じ単語を二度以上使うことは出来ません．{player}の負けです．")
        return False
    used_word.add(get_yomi(word))
    return True


def check_connect(prev_word: str, cur_word: str, cur_player: str) -> bool:
    if get_yomi(prev_word)[-1] != get_yomi(cur_word)[0]:
        print(f"> 前の言葉と繋がっていません．{cur_player}の負けです．")
        return False
    return True


def check_word_end(word: str, player: str) -> bool:
    if get_yomi(word)[-1] == "ン":
        print(f"> 'ん'で終わっています．{player}の負けです．")
        return False
    return True


def game() -> None:
    init = True  # 最初の一手は繫がり判定をしないためのフラグ
    while True:
        # User
        user_word = input("user:")
        if not check_history(user_word, "user"):
            return
        if init:
            cpu_word = get_yomi(user_word)[0]
            init = False
        if not check_connect(cpu_word, user_word, "user"):
            return
        if not check_word_end(user_word, "user"):
            return

        # CPU
        cpu_word = get_cpu_word(user_word)
        if cpu_word is None:
            print("> 思いつきません．cpuの負けです...")
            return
        print(f"cpu:{cpu_word}({get_yomi(cpu_word)})")
        if not check_connect(user_word, cpu_word, "cpu"):
            return
        if not check_word_end(cpu_word, "cpu"):
            return
        if not check_history(cpu_word, "cpu"):
            return


if __name__ == '__main__':
    game()
