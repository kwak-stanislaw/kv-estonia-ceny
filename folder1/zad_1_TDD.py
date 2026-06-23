"""
Build a function calculate(expression: str) -> float that evaluates simple math expressions passed as strings (min. two arguments).
like:
calculate("1 + 1") -> 2
calculate("2 * 2") -> 4

operands = +,-,*,/,**

Write ONE test at a time, after that write only enough code to make it pass before moving on to the next functionality.


* You can try, implement logic to handle more complex expressions like:
calculate("2 * 2 + 2 / 2")
funkcje pisać nad testem

"""

#import pytest


def test_addition():
    assert calculate("1 + 1") == 2

def test_subtraction():
    assert calculate("5 - 3") == 2

def test_multiplication():
    assert calculate("2 * 3") == 6

def test_dividing():
    assert calculate("9 / 3") == 3

def test_potegowanie():
    assert calculate("5**2") == 25


def calculate(expression: str) -> float:
    a, op, b = expression.split()
    a, b = float(a), float(b)

    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    if op == "**":
        return a ** b