from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import ServiceRequest, ServiceType, RequestAttachment, RequestStatusUpdate
from .forms import ServiceRequestForm, RequestStatusUpdateForm, SupportRequestUpdateForm

@login_required
def request_list(request):
    """View to display a list of customer's service requests"""
    # Get all service requests for the current user
    requests = ServiceRequest.objects.filter(customer=request.user).order_by('-created_at')
    
    return render(request, 'customer_service/request_list.html', {
        'requests': requests
    })

@login_required
def create_request(request):
    """View to create a new service request"""
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            # Create service request but don't save to DB yet
            service_request = form.save(commit=False)
            # Set the customer to the current user
            service_request.customer = request.user
            # Now save to DB
            service_request.save()
            
            # Handle file attachment
            if 'attachments' in request.FILES:
                file = request.FILES['attachments']
                RequestAttachment.objects.create(
                    service_request=service_request,
                    file=file,
                    filename=file.name
                )
            
            # Create initial status update
            RequestStatusUpdate.objects.create(
                service_request=service_request,
                previous_status='',
                new_status='pending',
                updated_by=request.user,
                notes='Service request created'
            )
            
            messages.success(request, f'Your service request has been created with reference number {service_request.request_number}')
            return redirect('request_detail', request_number=service_request.request_number)
    else:
        form = ServiceRequestForm()
    
    # Get all active service types
    service_types = ServiceType.objects.filter(is_active=True)
    
    return render(request, 'customer_service/create_request.html', {
        'form': form,
        'service_types': service_types
    })

@login_required
def request_detail(request, request_number):
    """View to display details of a specific service request"""
    # Get the service request, ensuring it belongs to the current user
    service_request = get_object_or_404(ServiceRequest, 
                                       request_number=request_number, 
                                       customer=request.user)
    
    # Get status updates for this request
    status_updates = service_request.status_updates.all().order_by('-created_at')
    
    # Get attachments for this request
    attachments = service_request.attachments.all()
    
    return render(request, 'customer_service/request_detail.html', {
        'service_request': service_request,
        'status_updates': status_updates,
        'attachments': attachments
    })

@staff_member_required
def support_dashboard(request):
    """Dashboard view for support staff"""
    # Get all service requests ordered by priority and creation time
    # We'll filter for status and priority in-code instead of using __in lookup
    # which isn't supported in the way it was initially written
    requests = ServiceRequest.objects.all().order_by('-created_at')
    
    # Filter requests if search query is provided
    search_query = request.GET.get('search', '')
    if search_query:
        requests = requests.filter(
            Q(request_number__icontains=search_query) |
            Q(customer__username__icontains=search_query) |
            Q(customer__email__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'all':
        requests = requests.filter(status=status_filter)
    
    # Get request counts by status for dashboard stats
    status_counts = ServiceRequest.objects.values('status').annotate(count=Count('status'))
    stats = {item['status']: item['count'] for item in status_counts}
    
    return render(request, 'customer_service/support_dashboard.html', {
        'requests': requests,
        'search_query': search_query,
        'status_filter': status_filter,
        'stats': stats
    })

@staff_member_required
def support_request_detail(request, request_number):
    """View for support staff to see details of a service request"""
    # Get the service request
    service_request = get_object_or_404(ServiceRequest, request_number=request_number)
    
    # Get status updates for this request
    status_updates = service_request.status_updates.all().order_by('-created_at')
    
    # Get attachments for this request
    attachments = service_request.attachments.all()
    
    # Create status update form
    if request.method == 'POST':
        status_form = RequestStatusUpdateForm(request.POST, service_request=service_request)
        if status_form.is_valid():
            status_update = status_form.save(commit=False)
            status_update.service_request = service_request
            status_update.previous_status = service_request.status
            status_update.updated_by = request.user
            
            # Update the service request status
            service_request.status = status_update.new_status
            service_request.save()
            
            # Save the status update
            status_update.save()
            
            messages.success(request, f'Status updated to {status_update.get_new_status_display()}')
            return redirect('support_request_detail', request_number=request_number)
    else:
        status_form = RequestStatusUpdateForm(service_request=service_request)
    
    # Create form for updating the request
    update_form = SupportRequestUpdateForm(instance=service_request)
    
    return render(request, 'customer_service/support_request_detail.html', {
        'service_request': service_request,
        'status_updates': status_updates,
        'attachments': attachments,
        'status_form': status_form,
        'update_form': update_form
    })

@staff_member_required
def update_request(request, request_number):
    """View for support staff to update a service request"""
    # Get the service request
    service_request = get_object_or_404(ServiceRequest, request_number=request_number)
    
    if request.method == 'POST':
        form = SupportRequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            # Get the old status before saving
            old_status = service_request.status
            
            # Save the form
            updated_request = form.save()
            
            # If status has changed, create a status update
            if old_status != updated_request.status:
                RequestStatusUpdate.objects.create(
                    service_request=updated_request,
                    previous_status=old_status,
                    new_status=updated_request.status,
                    updated_by=request.user,
                    notes=request.POST.get('status_notes', '')
                )
            
            messages.success(request, f'Service request {service_request.request_number} has been updated')
            return redirect('support_request_detail', request_number=request_number)
    else:
        form = SupportRequestUpdateForm(instance=service_request)
    
    return render(request, 'customer_service/update_request.html', {
        'form': form,
        'service_request': service_request
    })
