"""
Write a function get_first(lst) that returns the first element of a list,
but raises ValueError with message "List is empty" if the list is empty. Write tests for both paths.
"""
import pytest

def get_first(lst):
    if not lst:
        raise ValueError("List is empty")
    return lst[0]


def test_get_first_valid():
    assert get_first([1, 2, 3]) == 1


def test_get_first_empty():
    with pytest.raises(ValueError, match="List is empty"):
        get_first([])