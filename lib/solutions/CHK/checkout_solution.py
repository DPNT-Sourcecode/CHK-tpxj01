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

    def get_discount(self) -> int:
        raise NotImplementedError

class QuantityDiscountOffer(Offer):

    def __init__(self, item: Item, quantity: int, price: int):
        super().__init__(item)
        self.quantity = quantity
        self.price = price

    def get_discount(self) -> int:
        return (self.item.price * self.quantity) - self.price


class OtherItemFreeOffer(Offer):
    pass # TODO


class CheckoutSolution:

    def __init__(self):
        # Build our product catalogue
        self.catalogue = Catalogue()
        a = Item("A", 50)
        b = Item("B", 30)
        c = Item("C", 20)
        d = Item("D", 15)
        self.catalogue.add_item(a)
        self.catalogue.add_item(b)
        self.catalogue.add_item(c)
        self.catalogue.add_item(d)

        self.offers = {}
        self.offers[a.sku] = [QuantityDiscountOffer(a, 5, 200), QuantityDiscountOffer(a, 3, 130)]
        self.offers[b.sku] = [QuantityDiscountOffer(b, 2, 45)]


    # skus = unicode string
    def checkout(self, skus):
        # Map of sku to quantity
        basket = {}

        for sku in skus:
            basket[sku] = basket.get(sku, 0) + 1

        total = 0
        for sku, quantity in basket.items():
            catalog_item = self.catalogue.items.get(sku)
            if not catalog_item:
                return -1

            item_price = catalog_item.price
            sku_total = item_price * quantity

            # Apply any offers to this SKU by applying the discount
            if self.offers.get(sku):
                for offer in self.offers[sku]:
                    discount = offer.get_discount()
                    sku_total -= (discount * math.floor(quantity / self.offers[sku].quantity))

            total += sku_total

        return total


