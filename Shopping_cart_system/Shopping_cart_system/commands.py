from abc import ABC, abstractmethod
from Shopping_cart_system.models import CartItem,Product
from django.http import HttpResponseBadRequest

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class ViewCartCommand(Command):
    def __init__(self, cart):
        self.cart = cart
    #Executes the command to view cart items
    def execute(self):
        return self.cart.cartitem_set.all() #returns all cart items

class AddToCartCommand(Command):
    def __init__(self, cart, product, quantity):
        self.cart = cart
        self.product = product
        self.quantity = quantity
    #Executes the command to add cart items
    def execute(self):
        cart_item, created = CartItem.objects.get_or_create(cart=self.cart, product=self.product) # getting cart instance
        cart_item.quantity = self.quantity
        cart_item.save()


class RemoveFromCartCommand(Command):
    #Command to remove cart items
    def __init__(self, cart, product, quantity):
        self.cart = cart
        self.product = product
        self.quantity = quantity

    def execute(self):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=self.product) # getting cart item
            if cart_item.quantity > self.quantity:
                cart_item.quantity -= self.quantity
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            raise HttpResponseBadRequest("The item is not in the cart.") 

class ViewProductsCommand(Command):
    #Command to view all products
    def __init__(self, category):
        self.category = category

    def execute(self):
        products = Product.objects.filter(category=self.category)
        return products
