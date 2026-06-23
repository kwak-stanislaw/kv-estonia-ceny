"""
ShoppingCart class have two methods: add(item, price) and total().
Write a fixture that creates a cart with 2 items already added. Use that fixture in at least 2 tests.
"""

import pytest

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, item, price):
        self.items.append({"item": item, "price": price})

    def total(self):
        return sum(i["price"] for i in self.items)

@pytest.fixture
def cart():
    c = ShoppingCart()
    c.add("jablko", 2)
    c.add("banan", 3)
    return c


def test_total(cart):
    assert cart.total() == 5


def test_items_count(cart):
    assert len(cart.items) == 2