from solutions.CHK.checkout_solution import CheckoutSolution

import pytest

class TestCheckout:

    @pytest.mark.parametrize("sku,price", [
        ("A", 50),
        ("B", 30),
        ("C", 20),
        ("D", 15),
    ])
    def test_one_item(self, sku, price):
        assert CheckoutSolution().checkout(sku) == price

    def test_multiple_items(self):
        assert CheckoutSolution().checkout("ABCD") == 115

    def test_offers(self):
        # 130 + 30 + 20 + 15
        assert CheckoutSolution().checkout("ABCADA") == 195