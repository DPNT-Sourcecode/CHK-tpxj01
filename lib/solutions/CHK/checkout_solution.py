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

    def apply_to(self, basket) -> int:
        raise NotImplementedError

class QuantityDiscountOffer(Offer):

    def __init__(self, item: Item, quantity_prices: list[tuple[int, int]]):
        super().__init__(item)
        self.quantity_prices = quantity_prices

    def apply_to(self, basket) -> int:
        num_times_to_apply_discount = math.floor(remaining_quantity / offer.quantity)
        # sku_total -= (discount * num_times_to_apply_discount)
        # remaining_quantity -= (num_times_to_apply_discount * offer.quantity)

        return (self.item.price * self.quantity) - self.price


class OtherItemFreeOffer(Offer):
    def __init__(self, item: Item, quantity: int, free_item: Item):
        super().__init__(item)
        self.quantity = quantity
        self.free_item = free_item

    def apply_to(self, basket) -> int:
        return 0 # TODO


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

        self.offers = {}
        self.offers[a.sku] = [QuantityDiscountOffer(
            item=a,
            quantity_prices=[
                (5, 200),
                (3, 130)]
        )]
        self.offers[b.sku] = [QuantityDiscountOffer(b, [(2, 45)])],
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
                    discount = offer.apply_to(basket)

                    # num_times_to_apply_discount = math.floor(remaining_quantity / offer.quantity)
                    # sku_total -= (discount * num_times_to_apply_discount)
                    # remaining_quantity -= (num_times_to_apply_discount * offer.quantity)

            total += sku_total

        return total

