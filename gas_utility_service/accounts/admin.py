from django.contrib import admin
from .models import CustomerProfile

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'address', 'phone_number')
    search_fields = ('user__username', 'user__email', 'account_number', 'phone_number')
