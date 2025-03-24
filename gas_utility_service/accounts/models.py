from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    """Model for storing additional information about customers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_number = models.CharField(max_length=20, unique=True, help_text="Customer's gas utility account number")
    address = models.TextField(help_text="Customer's residential address")
    phone_number = models.CharField(max_length=15, help_text="Customer's contact phone number")
    
    # For support staff to add notes about the customer
    customer_notes = models.TextField(blank=True, help_text="Notes about the customer (only visible to support staff)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.account_number}"
    
    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"
