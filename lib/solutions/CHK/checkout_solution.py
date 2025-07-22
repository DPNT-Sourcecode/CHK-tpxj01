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
    def __init__(self, item: Item, quantity: int, price: int):
        self.item = item
        self.quantity = quantity
        self.price = price

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

        # I have a feeling offers could get quite complex, so I'll start with something simple
        self.offers = {}
        self.offers[a.sku] = Offer(a, 3, 130)
        self.offers[b.sku] = Offer(b, 2, 45)


    # skus = unicode string
    def checkout(self, skus):
        # skus is "a string containing the SKUs of all the products in the basket"
        # Space separated? Comma separated?
        # Gonna assume they're not for now

        # "Sometimes, the requirements are unclear. Getting feedback from your users may be the key to moving
        # forward."
        # So to get feedback from "users", I need to "deploy to production"?

        # Map of sku to quantity
        basket = {}

        for sku in skus:
            if not sku.isalpha():
                return -1

            basket[sku] = basket.get(sku, 0) + 1

        total = 0
        for sku, quantity in basket.items():
            catalog_item = self.catalogue.items.get(sku)
            if catalog_item:
                item_price = catalog_item.price
                sku_total = item_price * quantity

                # Apply any offers to this SKU by applying the discount
                if self.offers.get(sku):
                    discount = (item_price * self.offers[sku].quantity) - self.offers[sku].price
                    sku_total -= (discount * math.floor(quantity / self.offers[sku].quantity))

                total += sku_total

        return total




