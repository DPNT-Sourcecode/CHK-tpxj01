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

class QuantityDiscountOffer(Offer):

    def __init__(self, item: Item, quantity: int, price: int):
        super().__init__(item)
        self.quantity = quantity
        self.price = price

    # Alternative approach

    # def apply_to(self, basket) -> int:
    #         item_quantity = basket[self.item.sku]
    #     remaining_quantity = item_quantity
    #     for offer_quantity, offer_price in self.quantity_prices:
    #         num_times_to_apply_discount = math.floor(remaining_quantity / offer_quantity)
    #         # sku_total -= (discount * num_times_to_apply_discount)
    #         # remaining_quantity -= (num_times_to_apply_discount * offer.quantity)
    #
    #     return (self.item.price * self.quantity) - self.price

    def get_discount(self) -> int:
        return (self.item.price * self.quantity) - self.price

    def applies_to(self, basket) -> bool:
        return basket[self.item.sku] >= self.quantity


class OtherItemFreeOffer(Offer):
    def __init__(self, item: Item, quantity: int, free_item: Item):
        super().__init__(item)
        self.quantity = quantity
        self.free_item = free_item

    def get_discount(self) -> int:
        return self.free_item.price

    def applies_to(self, basket) -> bool:
        return basket[self.item.sku] >= 2 and basket[self.free_item.sku] >= 1


class CheckoutSolution:

    def __init__(self):
        # Build our product catalogue
        self.catalogue = Catalogue()
        a = Item("A", 50)
        b = Item("B", 30)
        c = Item("C", 20)
        d = Item("D", 15)
        e = Item("E", 40)
        self.catalogue.add_item(a)
        self.catalogue.add_item(b)
        self.catalogue.add_item(c)
        self.catalogue.add_item(d)
        self.catalogue.add_item(e)

        self.offers = sorted([
            QuantityDiscountOffer(a, 5, 200)],
        key=lambda offer: offer.get_discount())
        self.offers[a.sku] = [QuantityDiscountOffer(a, 5, 200), QuantityDiscountOffer(a, 3, 130)]
        self.offers[b.sku] = [QuantityDiscountOffer(b, 2, 45)]
        self.offers[e.sku] = [OtherItemFreeOffer(e, 2, b)]


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
                remaining_quantity = quantity
                for offer in self.offers[sku]:
                    discount = offer.get_discount(basket)
                    num_times_to_apply_discount = math.floor(remaining_quantity / offer.quantity)
                    sku_total -= (discount * num_times_to_apply_discount)
                    remaining_quantity -= (num_times_to_apply_discount * offer.quantity)

            total += sku_total


            # TODO sort offers by potential discount
            # 5A for 200 = 50
            # 2E get one B free = 30
            # 3A for 130 = 20
            # 2B for 45 = 15
            # TODO Apply offer to basket, remove items to which offer has been applied
            # TODO continue to apply offers to the rest of the basket
            # e.g if you buy 2E and get one B free (discount = 30), you can't then get 2B for 45 (discount = 15)

        return total



