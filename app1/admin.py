from django.contrib import admin
from .models import Product, Cart, CartItem, Category, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms


# Register Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category', 'product_type', 'colors', 'storages', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        
        # Dynamically set the storage field's requirement based on category
        if self.instance.category and self.instance.category.name == 'Smartphone':
            # Make storage compulsory for smartphones
            self.fields['storages'].required = True
        else:
            # Make storage optional for chargers and accessories
            self.fields['storages'].required = False
            self.fields['storages'].widget = forms.HiddenInput()

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'description']
    list_editable = ['price', 'stock']
    search_fields = ['name']
    list_filter = ['price', 'category']
    ordering = ['name']
    fields = ['name', 'price', 'stock', 'category', 'product_type', 'colors', 'storages', 'description', 'image']
    
    # Use the custom form for Product admin
    form = ProductAdminForm

    def save_model(self, request, obj, form, change):
        # If no image is provided, set a default image
        if not obj.image:
            obj.image = 'path/to/default/image.jpg'  # Set default image if none is provided
        super().save_model(request, obj, form, change)




# Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created_at']
    search_fields = ['user__username', 'session_key']
    list_filter = ['created_at']


# CartItem Admin
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'color', 'storage']
    search_fields = ['product__name']
    list_filter = ['color', 'storage']


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_active']

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Register the models with the admin interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)  # Only register Product once
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Profile)
