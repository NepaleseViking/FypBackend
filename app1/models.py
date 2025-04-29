from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    SMARTPHONE = 'smartphone'
    ACCESSORY = 'accessory'
    CHARGER = 'charger'

    PRODUCT_TYPE_CHOICES = [
        (SMARTPHONE, 'Smartphone'),
        (ACCESSORY, 'Accessory'),
        (CHARGER, 'Charger'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="user_images/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPE_CHOICES,
        default=ACCESSORY,
    )
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    colors = models.CharField(max_length=100, default='')    # only one color
    storages = models.JSONField(default=list)  # List of available storage options for smartphones

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def clean(self):
        super().clean()
        if self.image:
            filename = self.image.name.lower()
            if not filename.endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Only JPG, JPEG, or PNG images are allowed.')

    def __str__(self):
        return self.name
    
 


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=30, blank=True)
    storage = models.CharField(max_length=30, blank=True)


METHOD = {

    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti")
}

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='app1_orders')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)
    

    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_placed")
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=15)


    def __str__(self):
        return f"Order #{self.id} by {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
