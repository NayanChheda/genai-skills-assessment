# challenges/level_1_basic/tests/test_string_utils.py
import pytest
from src.basics.string_utils import reverse_string, is_palindrome

def test_reverse_string() -> None:
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"

def test_is_palindrome() -> None:
    assert is_palindrome("radar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("") is True
    assert is_palindrome("a") is True