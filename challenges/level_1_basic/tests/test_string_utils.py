from src.basics.string_utils import reverse_string, is_palindrome


def test_reverse_string() -> None:
    """Test reverse_string function."""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"


def test_is_palindrome() -> None:
    """Test is_palindrome function."""
    assert is_palindrome("radar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("") is True
    assert is_palindrome("a") is True
