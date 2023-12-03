from abc import ABC, abstractmethod
from Shopping_cart_system.models import CartItem,Product

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddToCartCommand(Command):
    def __init__(self, cart, product, quantity):
        self.cart = cart
        self.product = product
        self.quantity = quantity

    def execute(self):
        cart_item, created = CartItem.objects.get_or_create(cart=self.cart, product=self.product)
        cart_item.quantity += self.quantity
        cart_item.save()


class RemoveFromCartCommand(Command):
    def __init__(self, cart, product, quantity):
        self.cart = cart
        self.product = product
        self.quantity = quantity

    def execute(self):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
            if cart_item.quantity > self.quantity:
                cart_item.quantity -= self.quantity
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass  # Handle the case where the item is not in the cart

class ViewProductsCommand(Command):
    def __init__(self, category):
        self.category = category

    def execute(self):
        products = Product.objects.filter(category=self.category)
        return products
