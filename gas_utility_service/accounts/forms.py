from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerProfile

class CustomerRegistrationForm(UserCreationForm):
    """Form for registering new customer accounts"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    account_number = forms.CharField(max_length=20, required=True, help_text="Your gas utility account number")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                account_number=self.cleaned_data['account_number'],
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number']
            )
        
        return user

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating customer profile information"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
class CustomerProfileUpdateForm(forms.ModelForm):
    """Form for updating customer profile details"""
    class Meta:
        model = CustomerProfile
        fields = ('address', 'phone_number')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
