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
        #return basket.get(self.item.sku, -1) >= 2 and basket.get(self.free_item.sku, -1) >= 1
        return basket.get(self.item.sku, -1) + basket.get(self.free_item.sku, -1) >= (self.quantity + 1)

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
        self.catalogue.add_item(a)
        self.catalogue.add_item(b)
        self.catalogue.add_item(c)
        self.catalogue.add_item(d)
        self.catalogue.add_item(e)
        self.catalogue.add_item(f)

        # Sort offers by potential discount
        # 5A for 200 = 50
        # 2E get one B free = 30
        # 3A for 130 = 20
        # 2B for 45 = 15
        self.offers = sorted([
            QuantityDiscountOffer(a, 5, 200),
            QuantityDiscountOffer(a, 3, 130),
            QuantityDiscountOffer(b, 2, 45),
            OtherItemFreeOffer(e, 2, b),
            OtherItemFreeOffer(f, 2, f)
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
                print(f"Applying offer to {offer.item.sku}")
                print(f"Basket: {basket}")
                total += offer.apply(basket) # updates basket in-place
                print(f"total: {total}")

        # Now simply total up the remaining items in the basket
        for sku, quantity in basket.items():
            catalog_item = self.catalogue.items.get(sku)
            if not catalog_item:
                return -1

            total += catalog_item.price * quantity

        return total

