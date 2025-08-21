# challenges/level_1_basic/tests/test_string_utils.py

from src.basics.string_utils import reverse_string, is_palindrome


def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"


def test_is_palindrome():
    assert is_palindrome("madam")
    assert is_palindrome("racecar")
    assert not is_palindrome("hello")
