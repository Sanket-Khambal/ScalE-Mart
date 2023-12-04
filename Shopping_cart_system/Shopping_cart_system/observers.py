from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from Shopping_cart_system.models import Product, Cart
from Shopping_cart_system.commands import ViewCartCommand
from django.contrib import messages
import random

class CartObserver(ABC):
    @abstractmethod
    def notify(self, request, total_price):
        pass

class BudgetExceededObserver(CartObserver):
    def notify(self, request, total_price):
        user_budget = request.user.userprofile.budget
        if total_price > user_budget:
            messages.warning(request,f'Warning: Your total cart price ({total_price}) has exceeded your budget ({user_budget}).')

def simulate_change_in_price(cart_items):
    if len(cart_items) < 2:
        return True

class PriceDecreasedObserver(CartObserver):
    def notify(self, request, total_price):
        products = Product.objects.all()
        selected_product = random.choice(products)
        original_price = selected_product.price
        user_cart,created = Cart.objects.get_or_create(user=request.user)
        view_cart_command = ViewCartCommand(cart=user_cart)
        cart_items = view_cart_command.execute()

        if simulate_change_in_price(cart_items=cart_items):
            new_price = original_price - 2
            selected_product.price = new_price
            selected_product.save()
            messages.info(request, f'The price of {selected_product.name} has decreased from {original_price} to {new_price}! Add to your cart now!!')

