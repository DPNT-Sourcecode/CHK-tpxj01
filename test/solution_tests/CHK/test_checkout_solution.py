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

    def test_unknown_item(self):
        assert CheckoutSolution().checkout("X") == -1

    def test_invalid_sku(self):
        assert CheckoutSolution().checkout("-") == -1

    def test_zero_items(self):
        assert CheckoutSolution().checkout("") == 0

    def test_multiple_items(self):
        assert CheckoutSolution().checkout("ABCD") == 115

    def test_quantity_discount_offer(self):
        assert CheckoutSolution().checkout("AAA") == 130
        # 130 + 30 + 20 + 15
        assert CheckoutSolution().checkout("ABCADA") == 195
        # 2 x A = 100
        # 4 x B = (45 * 2) = 90
        # 1 x C = 20
        # 1 x D = 15
        assert CheckoutSolution().checkout("ABCABDBB") == 225
        # 9 x A = 200 (for 5) + 130 (for 3) + 50 (for 1)
        # 1 x B = 30
        # 1 x C = 20
        assert CheckoutSolution().checkout("AABACAAAAAA") == 430
        # 200 + 200 + 200 + 130 + 50
        assert CheckoutSolution().checkout("AAAAAAAAAAAAAAAAAAA") == 780

    def test_free_item_offer(self):
        # 1A + 2E      + 1B  (one B deducted)
        # 50 + 40 + 40 + 30
        assert CheckoutSolution().checkout("AEBEB") == 160

    def test_free_item_and_quantity_discount_offer(self):
        # 2E      + 2B
        # 40 + 40 + 45
        assert CheckoutSolution().checkout("EEBBB") == 125


    def test_buy_two_f_get_one_f_free(self):
        assert CheckoutSolution().checkout("F") == 10
        assert CheckoutSolution().checkout("FF") == 20
        assert CheckoutSolution().checkout("FFF") == 20