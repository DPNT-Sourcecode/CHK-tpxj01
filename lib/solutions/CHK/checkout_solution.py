import math
from typing import Optional


class Item:
    def __init__(self, sku: str, price: int):
        self.sku = sku
        self.price = price


class Catalogue:
    def __init__(self):
        self.items = {}

    def add_item(self, item: Item):
        self.items[item.sku] = item

    def get_item(self, sku: str) -> Optional[Item]:
        return self.items.get(sku)

class Offer:
    def __init__(self, item: Item):
        self.item = item

    def get_discount(self, basket) -> int:
        raise NotImplementedError

    def applies_to(self, basket) -> bool:
        raise NotImplementedError

    def apply(self, basket) -> bool:
        raise NotImplementedError

class QuantityDiscountOffer(Offer):

    def __init__(self, item: Item, quantity: int, price: int):
        super().__init__(item)
        self.quantity = quantity
        self.price = price

    def get_discount(self, basket) -> int:
        return (self.item.price * self.quantity) - self.price

    def applies_to(self, basket) -> bool:
        return basket.get(self.item.sku, -1) >= self.quantity

    def apply(self, basket) -> int:
        basket[self.item.sku] -= self.quantity
        return self.price


class MultipleItemQuantityDiscount(Offer):

    def __init__(self, items: list[Item], quantity: int, price: int):
        self.items = items
        self.items.sort(key=lambda item: item.price, reverse=True)
        self.quantity = quantity
        self.price = price

    def get_discount(self, basket) -> int:
        # TODO we would need to modify this to ensure that the solution would work if either S, T, X, Y or Z had another offer.
        #  Because this offer is the only one that applies to any of them, we don't need this right now.

        return self.items[0].price * self.quantity

    def applies_to(self, basket) -> bool:
        num_applicable_items = 0
        for item in self.items:
            if basket.get(item.sku):
                num_applicable_items += basket[item.sku]
        print(f"applies if {num_applicable_items} >= {self.quantity}")
        return num_applicable_items >= self.quantity

    def apply(self, basket) -> int:
        print(f"applying offer, items: {[item.sku for item in self.items]}")
        applicable_basket_items = self.get_basket_items_used_in_offer(basket)

        for applicable_item_sku, applicable_item_quantity in applicable_basket_items.items():
            basket[applicable_item_sku] -= applicable_item_quantity

        return self.price

    def get_basket_items_used_in_offer(self, basket):
        applicable_items = {}
        for item in self.items:
            if basket.get(item.sku) and sum(applicable_items.values()) < self.quantity:
                applicable_items[item.sku] = min(basket.get(item.sku), self.quantity - sum(applicable_items.values()))
                print(f"added {applicable_items[item.sku]} of {item.sku}")
        print(f"applicable items in basket: {applicable_items}")
        return applicable_items


class OtherItemFreeOffer(Offer):
    def __init__(self, item: Item, quantity: int, free_item: Item):
        super().__init__(item)
        self.quantity = quantity
        self.free_item = free_item

    def get_discount(self, basket) -> int:
        return self.free_item.price

    def applies_to(self, basket) -> bool:
        if basket.get(self.item.sku) and basket.get(self.free_item.sku):
            if self.item.sku == self.free_item.sku:
                return basket[self.item.sku] >= self.quantity + 1
            return basket[self.item.sku] >= self.quantity and basket[self.free_item.sku] >= 1
        return False

    def apply(self, basket) -> int:
        basket[self.item.sku] -= self.quantity
        basket[self.free_item.sku] -= 1
        return self.item.price * self.quantity


class CheckoutSolution:

    def __init__(self):
        # Build our product catalogue
        self.catalogue = Catalogue()
        a = Item("A", 50)
        b = Item("B", 30)
        c = Item("C", 20)
        d = Item("D", 15)
        e = Item("E", 40)
        f = Item("F", 10)
        g = Item("G", 20)
        h = Item("H", 10)
        i = Item("I", 35)
        j = Item("J", 60)
        k = Item("K", 70)
        l = Item("L", 90)
        m = Item("M", 15)
        n = Item("N", 40)
        o = Item("O", 10)
        p = Item("P", 50)
        q = Item("Q", 30)
        r = Item("R", 50)
        s = Item("S", 20)
        t = Item("T", 20)
        u = Item("U", 40)
        v = Item("V", 50)
        w = Item("W", 20)
        x = Item("X", 17)
        y = Item("Y", 20)
        z = Item("Z", 21)

        self.catalogue.add_item(a)
        self.catalogue.add_item(b)
        self.catalogue.add_item(c)
        self.catalogue.add_item(d)
        self.catalogue.add_item(e)
        self.catalogue.add_item(f)
        self.catalogue.add_item(g)
        self.catalogue.add_item(h)
        self.catalogue.add_item(i)
        self.catalogue.add_item(j)
        self.catalogue.add_item(k)
        self.catalogue.add_item(l)
        self.catalogue.add_item(m)
        self.catalogue.add_item(n)
        self.catalogue.add_item(o)
        self.catalogue.add_item(p)
        self.catalogue.add_item(q)
        self.catalogue.add_item(r)
        self.catalogue.add_item(s)
        self.catalogue.add_item(t)
        self.catalogue.add_item(u)
        self.catalogue.add_item(v)
        self.catalogue.add_item(w)
        self.catalogue.add_item(x)
        self.catalogue.add_item(y)
        self.catalogue.add_item(z)


    # skus = unicode string
    def checkout(self, skus):
        total = 0

        # Populate our basket as map of sku to quantity
        basket = {}
        for sku in skus:
            basket[sku] = basket.get(sku, 0) + 1

        # Sort offers by potential discount
        # 5A for 200 = 50
        # 2E get one B free = 30
        # 3A for 130 = 20
        # 2B for 45 = 15
        # etc
        # TODO refactor to use sort(reverse=True)
        offers = sorted([
            QuantityDiscountOffer(quantity=5, item=self.catalogue.get_item("A"), price=200),
            QuantityDiscountOffer(quantity=3, item=self.catalogue.get_item("A"), price=130),
            QuantityDiscountOffer(quantity=2, item=self.catalogue.get_item("B"), price=45),
            OtherItemFreeOffer(quantity=2, item=self.catalogue.get_item("E"), free_item=self.catalogue.get_item("B")),
            OtherItemFreeOffer(quantity=2, item=self.catalogue.get_item("F"), free_item=self.catalogue.get_item("F")),
            QuantityDiscountOffer(quantity=5, item=self.catalogue.get_item("H"), price=45),
            QuantityDiscountOffer(quantity=10, item=self.catalogue.get_item("H"), price=80),
            QuantityDiscountOffer(quantity=2, item=self.catalogue.get_item("K"), price=120),
            OtherItemFreeOffer(quantity=3, item=self.catalogue.get_item("N"), free_item=self.catalogue.get_item("M")),
            QuantityDiscountOffer(quantity=5, item=self.catalogue.get_item("P"), price=200),
            QuantityDiscountOffer(quantity=3, item=self.catalogue.get_item("Q"), price=80),
            OtherItemFreeOffer(quantity=3, item=self.catalogue.get_item("R"), free_item=self.catalogue.get_item("Q")),
            OtherItemFreeOffer(quantity=3, item=self.catalogue.get_item("U"), free_item=self.catalogue.get_item("U")),
            QuantityDiscountOffer(quantity=2, item=self.catalogue.get_item("V"), price=90),
            QuantityDiscountOffer(quantity=3, item=self.catalogue.get_item("V"), price=130),
            MultipleItemQuantityDiscount(quantity=3, items=[
                self.catalogue.get_item("S"),
                self.catalogue.get_item("T"),
                self.catalogue.get_item("X"),
                self.catalogue.get_item("Y"),
                self.catalogue.get_item("Z")],
                price=45,
            )
        ],
            key=lambda offer: offer.get_discount(basket))
        offers.reverse()

        # Apply each offers to basket, removing items to which an offer has been applied
        # This ensure we don't apply multiple offers using the same items
        for offer in offers:
            while offer.applies_to(basket):
                # print(f"Applying offer to {offer.item.sku}")
                # print(f"Basket: {basket}")
                total += offer.apply(basket) # updates basket in-place
                # print(f"total: {total}")

        # Now simply total up the remaining items in the basket
        for sku, quantity in basket.items():
            catalog_item = self.catalogue.items.get(sku)
            if not catalog_item:
                return -1

            total += catalog_item.price * quantity

        return total


