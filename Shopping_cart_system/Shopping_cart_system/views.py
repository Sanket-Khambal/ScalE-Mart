from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Cart, Product
from Shopping_cart_system.commands import AddToCartCommand
from Shopping_cart_system.strategies import DefaultPriceCalculationStrategy,DiscountPriceCalculationStrategy,CouponDiscountStrategy,CreditCardPaymentStrategy,PayPalPaymentStrategy

def home(request):
    return render(request,'home.html')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    strategy = DefaultPriceCalculationStrategy()
    command = AddToCartCommand(cart, product, quantity=1, strategy=strategy)
    command.execute()
    return redirect('cart')



@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    # Apply discount strategies
    discount_strategy = DiscountPriceCalculationStrategy(DefaultPriceCalculationStrategy(), discount_percentage=10)

    # Apply coupon discount if a coupon code is provided
    coupon_code = request.GET.get('coupon_code')
    if coupon_code:
        coupon_strategy = CouponDiscountStrategy(discount_strategy, coupon_code, discount_percentage=20)
        total_price = sum(coupon_strategy.calculate_price(item.product, item.quantity) for item in cart_items)
    else:
        total_price = sum(discount_strategy.calculate_price(item.product, item.quantity) for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request, payment_method):
    cart = Cart()
    cart_items = cart.get_items()

    # Payment strategy
    if payment_method == 'credit_card':
        payment_strategy = CreditCardPaymentStrategy()
    elif payment_method == 'paypal':
        payment_strategy = PayPalPaymentStrategy()
    else:
        return HttpResponseBadRequest("Invalid payment method")

    total_price = sum(item['product'].price * item['quantity'] for item in cart_items)

    # Process payment
    payment_result = payment_strategy.process_payment(total_price)

    # Additional checkout logic (e.g., order creation, inventory update)

    # Clear the cart after checkout
    cart.clear_cart()

    return render(request, 'checkout.html', {'payment_result': payment_result})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page or another desired destination
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page or another desired destination
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


