from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=500)
    image = models.ImageField(upload_to='category', blank=True, null=True)  # Category image field

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to='product', blank=True, null=True)  # Product image field
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, unique=True)  # Unique identifier for each cart
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference to Product
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Reference to Cart
    quantity = models.IntegerField(default=0)  # Quantity of product
    active = models.BooleanField(default=True)  # Whether the item is active in the cart

    def sub_total(self):
        """Calculate the subtotal for this item."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
