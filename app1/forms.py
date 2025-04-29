from django import forms
from django.contrib.auth.models import User
from .models import Profile, Order
import os
from .models import Product

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) <= 2:
            raise forms.ValidationError("Password must be more than 2 characters.")
        return password
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Only JPG and PNG files are allowed for profile pictures.")
        return image
    
class SellerProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['seller']


class CheckoutForm(forms.ModelForm):
    ordered_by = forms.CharField(max_length=255, label="Ordered By", required=True)
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address", 
                  "mobile", "email", "payment_method"]
