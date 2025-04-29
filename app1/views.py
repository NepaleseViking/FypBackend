from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.contrib.auth.models import User
from .models import Product
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.core.files.images import get_image_dimensions
from .forms import SellerProductForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from django.views import View
from .forms import CheckoutForm
from django.urls import reverse


import os, requests, json

from .models import *

a = Product.objects.all()

print(f"products---->>>>>> {a}")

# Create your views here.


def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'seller/dashboard.html', {'products': products})

# Create new product
@login_required
def seller_product_create(request):
    if request.method == 'POST':
        form = SellerProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = SellerProductForm()
    return render(request, 'seller/product_form.html', {'form': form, 'title': 'Add Product'})

# Update product
@login_required
def seller_product_update(request, pk):
    product = Product.objects.get(pk=pk, seller=request.user)
    form = SellerProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('seller_dashboard')
    return render(request, 'seller/product_form.html', {'form': form, 'title': 'Edit Product'})

# Delete product
@login_required
def seller_product_delete(request, pk):
    product = Product.objects.get(pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')
    return render(request, 'seller/confirm_delete.html', {'product': product})


@login_required(login_url='Login') #this ensures that you need to login to go further the homepage
def HomePage(request):
    
    
    return render(request, 'Home.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')  # Use 'username' instead of 'Full Name'
        email = request.POST.get('email')
        pass1 = request.POST.get('password')  # Use 'password' instead of 'Password'

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
           return HttpResponse("User already exists, please try again!")  #if the username exists, this message will pop up

        # Create the user if the username is unique
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

        # Ensure the 'Seller' group exists
        seller_group, created = Group.objects.get_or_create(name='Seller')

        # Assign the user to the 'Seller' group if they selected the seller role
        if request.POST.get('role') == 'seller':
            my_user.groups.add(seller_group)

        return redirect('Login')  # This directs a fresh new created account to the login page

    return render(request, 'Sign.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('Full Name')  # This is the username field
        pass1 = request.POST.get('Password')  # This is the password field
        
        # Authenticate the user
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            # If the user is found, log them in
            login(request, user)
            
            # Check if the user is a seller or a regular user
            if user.groups.filter(name='Seller').exists():  # You should create a 'Seller' group for sellers
                return redirect('seller_dashboard')  # Redirect to the seller dashboard
            else:
                return redirect('Home')  # Redirect to the home page for regular users
        else:
            # If login fails
            return HttpResponse("Invalid credentials, please try again!")

    return render(request, 'Login.html')

def LogoutPage(request): #if this button is triggered, the system will logout
    logout(request)
    return redirect('Login')

def contact(request):
    return render(request, 'contact/contact.html') 

def product(request):
    return render(request, 'Product.html')

# views.py

def HomePage(request):
    return render(request, 'Home.html')

def category_view(request):
    return render(request, 'Categories.html')

def buy_now(request):
    product_id = request.GET.get('product')  # Get the product ID from the query parameter
    if product_id:
        product = get_object_or_404(Product, id=product_id)  # Fetch the product
        # Now, you can use 'product' and its attributes (like 'product.name', 'product.price', etc.)
        context = {
            'product': product,
        }
        return render(request, 'buy_page.html', context)
    else:
        return render(request, 'error_page.html', {'message': 'Product not found.'})

def cart_view(request):
    # Logic to retrieve cart items (if any) and pass them to the template
    return render(request, 'cart.html')

def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save the order to the database
            order = form.save()

            # Get the payment method chosen by the user
            pm = form.cleaned_data.get("payment_method")

            # If the payment method is Khalti, redirect to the Khalti request view with the order ID
            if pm == "khalti":
                # Make sure the redirection URL includes the correct order ID
                order_id = str(order.id)
                redirect_url = reverse("app1:khaltirequest")
                return redirect(redirect_url)

            # Otherwise, redirect to the payment page
            return redirect('Payment.html')  # Replace 'payment' with your actual payment URL name if needed
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})


def order_summary_view(request):
    return render(request, 'order-summary.html')


def qr_payment_view(request):
    return render(request, 'qr-payment.html')



def khalti_initiate_payment(request):
    if request.method == 'POST':
        # Print the entire POST data for debugging
        print(f"POST data: {request.POST}")

        # Extract total from the request data
        total = request.POST.get('total')

        # Check if the total is None or empty
        if not total:
            return JsonResponse({"error": "Total amount is required"}, status=400)

        try:
            # Try converting total to a float
            total = float(total)
        except ValueError:
            # If conversion fails, return an error response
            return JsonResponse({"error": "Invalid total amount"}, status=400)

        # Print the total on the server side for debugging
        print(f"Received total: {total}")

        # Get the logged-in user's details
        user = request.user

        # Try to get the name from first_name, last_name, or username
        name = user.get_full_name().strip()  # Using get_full_name() to get full name

        # Fallback to using first_name + last_name if full_name is empty
        if not name:
            name = f"{user.first_name} {user.last_name}".strip()

        # If the name is still missing, fallback to the username
        if not name:
            name = user.username

        email = user.email

        # Check if either name or email is missing and return a detailed error message
        if not name and not email:
            return JsonResponse({"error": "User details missing: both name and email are required"}, status=400)
        elif not name:
            return JsonResponse({"error": "User details missing: name is required"}, status=400)
        elif not email:
            return JsonResponse({"error": "User details missing: email is required"}, status=400)

        # Set the rest of the payment request data
        data = {
    "return_url": "http://127.0.0.1:8000/payment/success/",
    "cancel_url": "http://127.0.0.1:8000/order-summary/",  # 👈 Add this line
    "website_url": "http://127.0.0.1:8000/",
    "amount": int(total * 100),
    "purchase_order_id": "Order01",
    "purchase_order_name": "Test Order",
    "customer_info": {
        "name": name,
        "email": email,
        "phone": "9800000001"
    },
    "amount_breakdown": [
        {"label": "Mark Price", "amount": int(total * 100) - 300},
        {"label": "VAT", "amount": 300}
    ],
    "product_details": [
        {
            "identity": "1234567890",
            "name": "Khalti logo",
            "total_price": int(total * 100),
            "quantity": 1,
            "unit_price": int(total * 100)
        }
    ],
    "merchant_username": "electronix",
    "merchant_extra": "meta-info"
}

        # Send the request to Khalti API
        url = "https://dev.khalti.com/api/v2/epayment/initiate/"
        headers = {
            "Authorization": "key 05bf95cc57244045b8df5fad06748dab",  # Replace with your real key
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if 'payment_url' in result:
            return redirect(result['payment_url'])  # ✅ Redirect user to Khalti
        else:
            return JsonResponse({"error": "Payment initiation failed", "details": result}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)





def payment_success(request):
    # Retrieve query parameters
    pidx = request.GET.get('pidx')
    transaction_id = request.GET.get('transaction_id')
    tidx = request.GET.get('tidx')
    txnId = request.GET.get('txnId')
    amount = request.GET.get('amount')
    total_amount = request.GET.get('total_amount')
    mobile = request.GET.get('mobile')
    status = request.GET.get('status')
    purchase_order_id = request.GET.get('purchase_order_id')
    purchase_order_name = request.GET.get('purchase_order_name')
    merchant_username = request.GET.get('merchant_username')
    merchant_extra = request.GET.get('merchant_extra')

    # Validate required fields
    if not all([pidx, transaction_id, tidx, txnId, amount, total_amount, mobile, status, purchase_order_id, purchase_order_name, merchant_username]):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    if purchase_order_id and purchase_order_id.startswith('Order'):
        purchase_order_id = int(purchase_order_id[5:])  # 'Order01' -> 1

    try:
        order = Order.objects.get(id=purchase_order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": f"Order with ID {purchase_order_id} not found"}, status=404)

    # ⚙️ Process session cart (not DB cart)
    session_cart = request.session.get('cart', [])
    for item in session_cart:
        try:
            product = Product.objects.get(id=item['id'])
            quantity = item['quantity']
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
            else:
                print(f"⚠️ Not enough stock for {product.name}")
        except Product.DoesNotExist:
            print(f"⚠️ Product with ID {item['id']} not found")

    # ✅ Clear the session cart
    request.session['cart'] = []

    user = order.ordered_by
    user_name = user.get_full_name() or f"{user.first_name} {user.last_name}"

    context = {
        'name': user_name,
        'pidx': pidx,
        'transaction_id': transaction_id,
        'tidx': tidx,
        'txnId': txnId,
        'amount': amount,
        'total_amount': total_amount,
        'mobile': mobile,
        'status': status,
        'purchase_order_id': purchase_order_id,
        'purchase_order_name': purchase_order_name,
        'merchant_username': merchant_username,
        'merchant_extra': merchant_extra
    }

    return render(request, 'payment_success.html', context)






# Khalti request view where the payment is processed
def khaltirequest_view(request):
    cart = get_user_cart(request)  # Get the user's cart
    total_amount = 0

    # Calculate the total amount of the items in the cart
    for item in cart.items.all():
        total_amount += item.product.price * item.quantity  # Assuming CartItem has 'product' and 'quantity'

    context = {
        'total_amount': total_amount,  # Pass the total amount to the template
    }

    return render(request, "khaltirequest.html", context)



def payment_view(request):
    # Your payment view logic here
    return render(request, "payment.html", {
        # context data goes here
    })

def buy_now(request):
    product_id = request.GET.get('product')

    # Recommendation logic (using name as the key)
    RECOMMENDATIONS = {
        'iphone14pro': ['iphone16', 'phonecase', 'wirelesscharger'],
        'iphone16': ['iphone14pro', 'fastcharger', 'wirelessheadphones'],
        'galaxys24': ['samsungcase', 'samsungcharger'],
        'redminote13pro': ['wirelesscharger', 'phonecase'],
    }

    try:
        # Use 'id' to get the product
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found.")

    # Fetch recommendations based on the product's name
    recommended_keys = RECOMMENDATIONS.get(product.name, [])  # Get recommendations based on name
    recommendations = Product.objects.filter(name__in=recommended_keys)  # Query products by name

    return render(request, 'buy.html', {
        'product': product, 
        'recommendations': recommendations,
    })

# Function to get the user's cart (for both logged-in users and guests)
def get_user_cart(request):
    user = request.user

    if user.is_authenticated:
        # Get the cart for logged-in users (based on User)
        cart, created = Cart.objects.get_or_create(user=user, session_key=None)
    else:
        # Get the cart for guests (based on session_key)
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Create a session if not already created
            session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)

    return cart


    from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product

# View for displaying products
def product_list(request):
    products = Product.objects.all()
    for product in products:
        if product.stock <= 0:
            product.status = 'Out of stock'
        elif product.stock <= 5:
            product.status = f'Only {product.stock} left'
        else:
            product.status = f'In stock'

    return render(request, 'product.html', {'products': products})

#View for products
def product_view(request):
    # Fetch all products
    products = Product.objects.all()

    selected_category = request.GET.get('category')

    if selected_category:
        products = products.filter(category__id=selected_category)
    else:
        products = Product.objects.all()
    
    # Fetch categories for the filter dropdown (if you have categories)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'product.html', context)


# View to show the products on the buy page
def buy_view(request):
    products = Product.objects.all()
    return render(request, 'Buy.html', {'products': products})
    


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    try:
        # Fetch the product from the database
        product = Product.objects.get(id=product_id)
        
        # Check if the product is in stock
        if product.stock <= 0:
            # Return a JSON response if the product is out of stock
            return JsonResponse({'error': 'Product is out of stock'}, status=400)
        
        # If the product is in stock, add it to the cart
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'img': product.image.url,
            'quantity': 1,  # You can modify this to add quantity based on user input
        })
        
        # Decrease stock when added to cart
        product.stock -= 1  
        product.save()

        # Save the cart to the session
        request.session['cart'] = cart
        
    except Product.DoesNotExist:
        # If product doesn't exist, return an error
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # Redirect to the cart page
    return redirect('cart')  # Replace with the actual cart page URL name

# Cart page view
def cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart': cart})


def category_view(request):
    categories = Category.objects.all()           # Get all categories (if needed for filter dropdown)
    products = Product.objects.all()              # Show all products by default

    selected_category_id = request.GET.get('category')  # Optional: Get category from URL query (?category=1)

    if selected_category_id:
        products = products.filter(category_id=selected_category_id)

    context = {
        'categories': categories,
        'products': products,
    }

    for i in products:
        print(f"-------->{i.image}.url")

    return render(request, 'Categories.html', context)









# This one is for the login profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app1.forms import ProfileForm

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if form.is_valid():
            # Get the cleaned data from the form
            new_name = form.cleaned_data['username']
            new_email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            new_image = form.cleaned_data['image']

            # Apply changes
            user.username = new_name
            user.email = new_email
            if new_password:
                user.set_password(new_password)
            user.save()

            # Handle image update
            if new_image:
                user.profile.image = new_image
            user.profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            # If the form is not valid, display the errors
            for field in form.errors:
                messages.error(request, f"{field}: {form.errors[field]}")
    else:
        form = ProfileForm(instance=user.profile)

    return render(request, 'profile.html', {'form': form})



def display_image(request, product_id):
    product = Product.objects.get(id=product_id)
    image_data = product.image.url
    # Set the content type to image
    return HttpResponse(image_data, content_type="image/jpeg")









