from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProductForm
from .models import Product

def home(request):
    product = Product.objects.all()
    return render(request, 'home.html', {'product': product})

def add_product(request):
    if request.method == "POST":
        productForm = ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
            return redirect('home')
    productForm = ProductForm()
    return render(request, 'add_product.html', {'form': productForm})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('home')
    product_form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': product_form})

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('home')

def demo(request):
    return render(request, 'demo.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        myuser = User.objects.create_user(username=username, password=password1, email=email)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        return redirect('signin')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Corrected to match form field name

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name
            return render(request, 'user_dashboard.html', {'fname': fname, 'lname': lname})
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return render(request,'home.html')