from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm, ProfileUpdateForm, CustomerProfileUpdateForm
from customer_service.models import ServiceRequest

def register(request):
    """View for registering new customers"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """View for displaying customer profile and service request history"""
    user = request.user
    
    # Get service requests for this user
    service_requests = ServiceRequest.objects.filter(customer=user).order_by('-created_at')
    
    context = {
        'user': user,
        'profile': user.profile,
        'service_requests': service_requests
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def update_profile(request):
    """View for updating customer profile information"""
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = CustomerProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = CustomerProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'accounts/profile.html', context)
