import pytest
from src.app import Game


def test_dict():
    game = Game()
    assert type(game._Game__dict) is dict
    assert type(game._Game__dict["ア"]) is list
    assert 1 <= len(game._Game__dict["ア"])
    with pytest.raises(KeyError):
        game._Game__dict["あ"]


def test_used_word():
    game = Game()
    assert len(game._Game__used_word) == 0
    game._Game__used_word.add("テスト")
    assert len(game._Game__used_word) == 1


def test_get_yomi_hira():
    assert Game().get_yomi("りんご") == "リンゴ"


def test_get_yomi_kana():
    assert Game().get_yomi("エラトステネス") == "エラトステネス"


def test_get_yomi_kanji():
    assert Game().get_yomi("部分分数分解") == "ブブンブンスウブンカイ"


def test_get_prefix_normal():
    assert Game().get_prefix("りんご") == "リ"


def test_get_prefix_extra():
    assert Game().get_prefix("社長") == "シャ"


def test_get_suffix_normal():
    assert Game().get_suffix("林檎") == "ゴ"


def test_get_suffix_extra():
    assert Game().get_suffix("隠居") == "キョ"


def test_get_cpu_word():
    game = Game()
    # tests/からsrc/を見ているので，そのままだとsrc/data/が参照できないっぽい
    # そのため，テストの時は最小の辞書(exceptの方)を使う
    assert game.get_cpu_word("しりとり") is None
    assert game.get_cpu_word("学校") == "嘘"


def test_check_word_end():
    assert Game().check_word_end("しりとり", "player") is True
    assert Game().check_word_end("みかん", "player") is False


def test_check_history():
    game = Game()
    assert game.check_history("しりとり", "player") is True
    assert game.check_history("しりとり", "player") is False


def test_check_connect():
    assert Game().check_connect("しりとり", "林檎", "player") is True
    assert Game().check_connect("しりとり", "ミカン", "player") is False
