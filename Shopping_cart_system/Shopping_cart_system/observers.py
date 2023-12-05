from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from Shopping_cart_system.models import Product, Cart
from Shopping_cart_system.commands import ViewCartCommand
from django.contrib import messages
import random

class CartObserver(ABC):
    # Interface for cart observers
    @abstractmethod
    def notify(self, request, total_price):
        pass

class BudgetExceededObserver(CartObserver):
    # Observer to check if the budget is exceeded
    def notify(self, request, total_price):
        user_budget = request.user.userprofile.budget
        if total_price > user_budget:
            messages.warning(request,f'Warning: Your total cart price ({total_price}) has exceeded your budget ({user_budget}).')

def simulate_change_in_price(cart_items):
    # function to check whether or not to simulate price change
    if len(cart_items) < 2:
        return True

class PriceDecreasedObserver(CartObserver):
    # Observer to send alerts for price drops
    def notify(self, request, total_price):
        products = Product.objects.all() # getting all products
        selected_product = random.choice(products) # randomly selecting a product
        original_price = selected_product.price
        user_cart,created = Cart.objects.get_or_create(user=request.user) # getting cart instance
        view_cart_command = ViewCartCommand(cart=user_cart)
        cart_items = view_cart_command.execute()

        if simulate_change_in_price(cart_items=cart_items):           # Changing product price
            new_price = original_price - 2
            selected_product.price = new_price
            selected_product.save()
            messages.info(request, f'The price of {selected_product.name} has decreased from {original_price} to {new_price}! Add to your cart now!!')

