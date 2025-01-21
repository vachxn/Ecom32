from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, Cart, CartItem


# Home view to display all products
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# Add a new product
def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Product added successfully.")
            return redirect('home')
    else:
        product_form = ProductForm()
    return render(request, 'add_product.html', {'form': product_form})


# Edit an existing product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('home')
    else:
        product_form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': product_form})


# Delete a product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('home')


# Demo view (optional)
def demo(request):
    return render(request, 'demo.html')


# User registration
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = fname
        user.last_name = lname
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect('signin')

    return render(request, 'signup.html')


# User login
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('signin')

    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'signin.html')


# User logout
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


# Generate or retrieve a cart ID
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Add an item to the cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, active=True)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    messages.success(request, "Item added to cart.")
    return redirect('view_cart')


# Remove an item from the cart
@login_required
def remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
    return redirect('view_cart')


# View the cart
@login_required
def view_cart(request):
    try:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        total = sum([item.sub_total() for item in cart_items])
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total': total})


# Checkout (placeholder)
@login_required
def checkout(request):
    messages.info(request, "Checkout functionality to be implemented.")
    return render(request, 'checkout.html')