import pytest

"""
Function `is_palindrome(s)` returns `True` if a string reads the same forwards and backwards. 
Write at least 3 tests: one with a palindrome, one without, and one for an empty string.
"""
def is_palindrome(s):
    return s == s[::-1]

def test_palindrome_true():
    assert is_palindrome("zaraz") is True

def test_palindrome_false():
    assert is_palindrome("hej") is False

def test_palindrome_empty_string():
    assert is_palindrome("") is True

    