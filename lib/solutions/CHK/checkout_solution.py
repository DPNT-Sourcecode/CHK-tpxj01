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
        self.catalogue.add_item(Item("A", 50))
        self.catalogue.add_item(Item("B", 30))
        self.catalogue.add_item(Item("C", 20))
        self.catalogue.add_item(Item("D", 15))


    # skus = unicode string
    def checkout(self, skus):
        # skus is "a string containing the SKUs of all the products in the basket"
        # Space separated? Comma separated?
        # Gonna assume they're not for now

        # "Sometimes, the requirements are unclear. Getting feedback from your users may be the key to moving
        # forward."
        # So to get feedback from "users", I need to "deploy to production"?

        total = 0
        for sku in skus:
            total += self.catalogue.items[sku].price
        return total

