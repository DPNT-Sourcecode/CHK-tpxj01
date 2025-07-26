import math

class Item:
    def __init__(self, sku: str, price: int):
        self.sku = sku
        self.price = price


class Catalogue:
    def __init__(self):
        self.items = {}

    def add_item(self, item: Item):
        self.items[item.sku] = item

class Offer:
    def __init__(self, item: Item):
        self.item = item

    def get_sku(self):
        return self.item.sku

    def get_discount(self) -> int:
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

    def get_discount(self) -> int:
        return (self.item.price * self.quantity) - self.price

    def applies_to(self, basket) -> bool:
        return basket.get(self.item.sku, -1) >= self.quantity

    def apply(self, basket) -> int:
        basket[self.item.sku] -= self.quantity
        return self.price


class OtherItemFreeOffer(Offer):
    def __init__(self, item: Item, quantity: int, free_item: Item):
        super().__init__(item)
        self.quantity = quantity
        self.free_item = free_item

    def get_discount(self) -> int:
        return self.free_item.price

    def applies_to(self, basket) -> bool:
        if basket.get(self.item.sku) and basket.get(self.free_item.sku):
            if self.item.sku == self.free_item.sku:
                return basket[self.item.sku] >= self.quantity + 1
            return basket[self.item.sku] >= 2 and basket[self.free_item.sku] >= 1
        return False

    def apply(self, basket) -> int:
        basket[self.item.sku] -= self.quantity
        basket[self.free_item.sku] -= 1
        return self.item.price * self.quantity


class CheckoutSolution:

    def __init__(self):
        # Build our product catalogue
        # +------+-------+------------------------+
        # | Item | Price | Special offers         |
        # +------+-------+------------------------+
        # | A    | 50    | 3A for 130, 5A for 200 |
        # | B    | 30    | 2B for 45              |
        # | C    | 20    |                        |
        # | D    | 15    |                        |
        # | E    | 40    | 2E get one B free      |
        # | F    | 10    | 2F get one F free      |
        # | G    | 20    |                        |
        # | H    | 10    | 5H for 45, 10H for 80  |
        # | I    | 35    |                        |
        # | J    | 60    |                        |
        # | K    | 80    | 2K for 150             |
        # | L    | 90    |                        |
        # | M    | 15    |                        |
        # | N    | 40    | 3N get one M free      |
        # | O    | 10    |                        |
        # | P    | 50    | 5P for 200             |
        # | Q    | 30    | 3Q for 80              |
        # | R    | 50    | 3R get one Q free      |
        # | S    | 30    |                        |
        # | T    | 20    |                        |
        # | U    | 40    | 3U get one U free      |
        # | V    | 50    | 2V for 90, 3V for 130  |
        # | W    | 20    |                        |
        # | X    | 90    |                        |
        # | Y    | 10    |                        |
        # | Z    | 50    |                        |
        # +------+-------+------------------------+
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
        k = Item("K", 80)
        l = Item("L", 90)
        m = Item("M", 15)
        n = Item("N", 40)
        o = Item("O", 10)
        p = Item("P", 50)
        q = Item("Q", 30)
        r = Item("R", 50)
        s = Item("S", 30)
        t = Item("T", 20)
        u = Item("U", 40)
        v = Item("V", 50)
        w = Item("W", 20)
        x = Item("X", 90)
        y = Item("Y", 10)
        z = Item("Z", 50)

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

        # Sort offers by potential discount
        # 5A for 200 = 50
        # 2E get one B free = 30
        # 3A for 130 = 20
        # 2B for 45 = 15
        self.offers = sorted([
            QuantityDiscountOffer(quantity=5, item=a, price=200),
            QuantityDiscountOffer(quantity=3, item=a, price=130),
            QuantityDiscountOffer(quantity=2, item=b, price=45),
            OtherItemFreeOffer(quantity=2, item=e, free_item=b),
            OtherItemFreeOffer(quantity=2, item=f, free_item=f),
            QuantityDiscountOffer(quantity=5, item=h, price=45),
            QuantityDiscountOffer(quantity=10, item=h, price=80),
            QuantityDiscountOffer(quantity=2, item=k, price=150),
            OtherItemFreeOffer(quantity=3, item=n, free_item=m),
            QuantityDiscountOffer(quantity=5, item=p, price=200),
            QuantityDiscountOffer(quantity=3, item=q, price=80),
            OtherItemFreeOffer(quantity=3, item=r, free_item=q),
            OtherItemFreeOffer(quantity=3, item=u, free_item=u),
            QuantityDiscountOffer(quantity=2, item=v, price=90),
            QuantityDiscountOffer(quantity=3, item=v, price=130),
            ],
        key=lambda offer: offer.get_discount())
        self.offers.reverse()


    # skus = unicode string
    def checkout(self, skus):

        # Populate our basket as map of sku to quantity
        basket = {}
        for sku in skus:
            basket[sku] = basket.get(sku, 0) + 1

        total = 0

        # Apply each offers to basket, removing items to which an offer has been applied
        # This ensure we don't apply multiple offers using the same items
        for offer in self.offers:
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



