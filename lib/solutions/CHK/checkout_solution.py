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
        return basket.get(self.item.sku, -1) >= 2 and basket.get(self.free_item.sku, -1) >= 1

    def apply(self, basket) -> int:
        basket[self.item.sku] -= self.quantity
        basket[self.free_item.sku] -= 1
        return (self.item.price * self.quantity) + self.free_item.price


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

        # Sort offers by potential discount
        # 5A for 200 = 50
        # 2E get one B free = 30
        # 3A for 130 = 20
        # 2B for 45 = 15
        self.offers = sorted([
            QuantityDiscountOffer(a, 5, 200),
            QuantityDiscountOffer(a, 3, 130),
            QuantityDiscountOffer(b, 2, 45),
            OtherItemFreeOffer(e, 2, b)
            ],
        key=lambda offer: offer.get_discount())


    # skus = unicode string
    def checkout(self, skus):
        # Map of sku to quantity
        basket = {}

        for sku in skus:
            basket[sku] = basket.get(sku, 0) + 1

        total = 0

        # Apply each offers to basket, removing items to which an offer has been applied
        # This ensure we don't apply multiple offers using the same items
        for offer in self.offers:
            while offer.applies_to(basket):
                print(f"Applying offer to {offer.item.sku}")
                total += offer.apply(basket) # updates basket in-place

        # Now simply total up the remaining items in the basket
        for sku, quantity in basket.items():
            catalog_item = self.catalogue.items.get(sku)
            if not catalog_item:
                return -1

            total += catalog_item.price * quantity

            # # Apply any offers to this SKU by applying the discount
            # if self.offers.get(sku):
            #     remaining_quantity = quantity
            #     for offer in self.offers[sku]:
            #         discount = offer.get_discount(basket)
            #         num_times_to_apply_discount = math.floor(remaining_quantity / offer.quantity)
            #         sku_total -= (discount * num_times_to_apply_discount)
            #         remaining_quantity -= (num_times_to_apply_discount * offer.quantity)
            #
            # total += sku_total




        return total



