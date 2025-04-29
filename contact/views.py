from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .forms import ContactForm
from .models import ContactMessage
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from .models import Product



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            message = form.cleaned_data['message']
            EmailMessage(
                'Contact Form Submission{}'.format(name),
                message,
                'form-response@example.com',
                ['test.qpasa330@gmail.com'],
                [],
                reply_to=[email]
            ).send()
            return redirect('success')
        else:
            form = ContactForm()
        return render(request, 'contact.html', {'form': form})
    

def success(request):
    return HttpResponse('Success!')    






@login_required  # Ensure that the user is logged in before they can checkout
def checkout(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        total_price = request.POST['total_price']  # The price from your frontend

        # Create the order
        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            address=address,
            phone=phone,
            total_price=total_price
        )

        # Add each item to the order
        # You would likely pull this from the session or the frontend data
        cart_items = request.session.get('cart', [])
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['quantity']
            )

        # Clear the cart from the session
        request.session['cart'] = []

        return redirect('payment')  # Redirect to a payment page or order confirmation page

    return render(request, 'checkout.html')

