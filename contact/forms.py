from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=255, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email'}))
    message = forms.CharField(label="Your Text", widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}))

