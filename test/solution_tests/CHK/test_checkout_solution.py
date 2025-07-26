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

    def test_invalid_sku(self):
        assert CheckoutSolution().checkout("x") == -1
        assert CheckoutSolution().checkout("-") == -1

    def test_zero_items(self):
        assert CheckoutSolution().checkout("") == 0

    def test_multiple_items(self):
        assert CheckoutSolution().checkout("ABCD") == 115

    def test_quantity_discount_offer(self):
        # assert CheckoutSolution().checkout("AAA") == 130
        # 130 + 30 + 20 + 15
        # assert CheckoutSolution().checkout("ABCADA") == 195
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
        assert CheckoutSolution().checkout("FFFF") == 30
        assert CheckoutSolution().checkout("FFFFF") == 40
        assert CheckoutSolution().checkout("FFFFFF") == 40

    def test_buy_three_r_get_one_q_free(self):
        assert CheckoutSolution().checkout("RRQ") == 130
        assert CheckoutSolution().checkout("RRRQ") == 150

    # IF I HAD MORE TIME I'd consider some sort of automated way of generating tests based on list of offers
    # The downside to that is that you then have logic in tests, which itself requires.....testing
    # But for a huge number of offers writing individual tests for each is tedious and error prone
    # LLMs can help with that (I'm not using one for this, because I assume I can't unless specifically told so)


    def test_all_of_the_offers(self):
        # I'm a bit confused. I have two test failures:
        # Result is: FAILED
        # Some requests have failed (2/141). Here are some of them:
        #
        # Test: CHK_R4_139 | Method: checkout | Params: ["ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        # Assertion: equals
        # Expected: 1880
        # Actual:   1835
        #
        # ----------------------------------------
        #
        # Test: CHK_R4_140 | Method: checkout | Params: ["LGCKAQXFOSKZGIWHNRNDITVBUUEOZXPYAVFDEPTBMQLYJRSMJCWH"]
        # Assertion: equals
        # Expected: 1880
        # Actual:   1835
        #
        # I have copied and pasted the params and expected values into the assertions below, and the tests pass.
        # Yet for some reason they fail when ran on the server. Did my code not "upload" to the server correctly?
        # I don't know how to debug this without getting more time penalties.

        # UPDATE: Thankfully these passed after submitting a second time
        assert CheckoutSolution().checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ") == 1768
        assert CheckoutSolution().checkout("LGCKAQXFOSKZGIWHNRNDITVBUUEOZXPYAVFDEPTBMQLYJRSMJCWH") == 1768

    # def test_buy_any_3_of_stxyz(self):
    #     assert CheckoutSolution().checkout("STXYZ") == 45