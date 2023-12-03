from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Cart, Product, CartItem
from Shopping_cart_system.commands import AddToCartCommand,ViewProductsCommand,ViewCartCommand,RemoveFromCartCommand
from Shopping_cart_system.strategies import DefaultPriceCalculationStrategy,DiscountPriceCalculationStrategy,CouponDiscountStrategy,CreditCardPaymentStrategy,PayPalPaymentStrategy,QuantityBasedDiscountStrategy

def home(request):
    return render(request,'home.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_home')  
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
            'total_price': item.product.price * item.quantity,
            'id':item.product.id
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
    
def remove_from_cart(request, product_id, quantity):
    product = Product.objects.get(pk=product_id)
    user_cart = Cart.objects.get(user=request.user)
    remove_command = RemoveFromCartCommand(cart=user_cart, product=product, quantity=quantity)
    remove_command.execute()
    return redirect('view_cart') 
    

def checkout(request):
    # Retrieve the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # View the cart to get the cart items
    view_cart_command = ViewCartCommand(cart=user_cart)
    cart_items = view_cart_command.execute()

    # Apply quantity-based discount strategy if there are more than four products
    quantity_discount_threshold = 4
    if len(cart_items) > quantity_discount_threshold:
        discount_strategy = QuantityBasedDiscountStrategy(DefaultPriceCalculationStrategy(), discount_threshold=quantity_discount_threshold, discount_percentage=15)
        discount_message = f'Quantity discount applied! Get {discount_strategy.discount_percentage}% off for purchasing more than {quantity_discount_threshold} products.'
    else:
        discount_strategy = DiscountPriceCalculationStrategy(DefaultPriceCalculationStrategy(), discount_percentage=10)
        discount_message = 'Default discount applied!'

    # Apply coupon discount if a coupon code is provided
    coupon_code = request.GET.get('coupon_code')
    if coupon_code:
        # Checking if the provided coupon code is valid
        coupon_strategy = CouponDiscountStrategy(discount_strategy, coupon_code, discount_percentage=20)
        if coupon_strategy.is_coupon_valid():
            total_price = sum(coupon_strategy.calculate_price(item.product, item.quantity) for item in cart_items)
            messages.success(request, f'Coupon "{coupon_code}" applied successfully! {discount_message}')
        else:
            total_price = sum(discount_strategy.calculate_price(item.product, item.quantity) for item in cart_items)
            messages.error(request, f'Invalid coupon code. {discount_message}')
    else:
        total_price = sum(discount_strategy.calculate_price(item.product, item.quantity) for item in cart_items)
        messages.success(request, discount_message)

    data = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', data)

