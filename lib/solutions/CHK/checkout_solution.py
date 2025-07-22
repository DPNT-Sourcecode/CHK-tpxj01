
class CheckoutSolution:

    class Item:
        def __init__(self, sku: str, price: int):
            self.sku = sku
            self.price = price


    class Inventory:
        def __init__(self):
            self.items = {}

        def add_item(self, item: Item):
            self.items[item.sku] = item


    # Not needed just yet, thinking ahead a bit
    # class Offer:
    #     def __init__(self, item: CheckoutSolution.Item, quantity: int, price: int):
    #         self.item = item
    #         self.quantity = quantity
    #         self.price = price


    # skus = unicode string
    def checkout(self, skus):
        # skus is "a string containing the SKUs of all the products in the basket"
        # Space separated? Comma separated?

        # "Sometimes, the requirements are unclear. Getting feedback from your users may be the key to moving
        # forward."
        # So to get feedback from "users", I need to "deploy to production"?

        raise NotImplementedError()




