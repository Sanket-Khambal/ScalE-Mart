from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Cart, Product, CartItem
from Shopping_cart_system.commands import AddToCartCommand,ViewProductsCommand,ViewCartCommand
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
            return redirect('user_home')  # Replace 'home' with the name of your home page or another desired destination
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def categories(request):
    unique_categories = Product.objects.values('category').distinct()
    return render(request, 'categories.html', {'categories': unique_categories})

def view_products_by_category(request, category):
    # Using the ViewProductsCommand to get products for the specified category
    view_command = ViewProductsCommand(category)
    products = view_command.execute()

    data = {
        'category': category,
        'products': products,
    }

    return render(request, 'products_by_category.html', data)

def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    view_cart_command = ViewCartCommand(cart=user_cart)
    cart_items = view_cart_command.execute()

    cart_items_data = [
        {
            'product_name': item.product.name,
            'quantity': item.quantity,
            'total_price': item.product.price * item.quantity
        }
        for item in cart_items
    ]

    total_price = sum(item['total_price'] for item in cart_items_data)

    context = {
        'cart_items_data': cart_items_data,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    # getting the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Getting the product based on the product_id
    product = Product.objects.get(pk=product_id)
    category = product.category

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        add_to_cart_command = AddToCartCommand(cart=user_cart, product=product, quantity=quantity)
        add_to_cart_command.execute()
        return redirect('products_by_category',category=category) 
