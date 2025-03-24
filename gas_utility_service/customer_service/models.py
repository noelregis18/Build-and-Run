from django.db import models
from django.contrib.auth.models import User
import uuid
import os

class ServiceType(models.Model):
    """Model for different types of service requests"""
    name = models.CharField(max_length=100, help_text="Name of the service type")
    description = models.TextField(help_text="Description of what this service type entails")
    is_active = models.BooleanField(default=True, help_text="Whether this service type is currently available")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Service Type"
        verbose_name_plural = "Service Types"

class ServiceRequest(models.Model):
    """Model for customer service requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]
    
    # Basic request information
    request_number = models.CharField(max_length=20, unique=True, editable=False,
                                    help_text="Unique identifier for the service request")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests',
                                help_text="Customer who submitted the request")
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name='requests',
                                    help_text="Type of service being requested")
    description = models.TextField(help_text="Detailed description of the service request")
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',
                            help_text="Current status of the request")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium',
                                help_text="Priority level of the request")
    
    # Support staff information
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='assigned_requests',
                                  help_text="Support staff member assigned to this request")
    support_notes = models.TextField(blank=True, 
                                  help_text="Internal notes for support staff (not visible to customer)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.request_number} - {self.customer.username}"
    
    def save(self, *args, **kwargs):
        # Generate unique request number on creation
        if not self.request_number:
            self.request_number = f"SR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Service Request"
        verbose_name_plural = "Service Requests"

def get_attachment_upload_path(instance, filename):
    """Generate upload path for request attachments"""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Return the upload path
    return os.path.join('request_attachments', instance.service_request.request_number, filename)

class RequestAttachment(models.Model):
    """Model for files attached to service requests"""
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=get_attachment_upload_path)
    filename = models.CharField(max_length=255, help_text="Original filename")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.filename} - {self.service_request.request_number}"
    
    def save(self, *args, **kwargs):
        if not self.filename and self.file:
            self.filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Request Attachment"
        verbose_name_plural = "Request Attachments"

class RequestStatusUpdate(models.Model):
    """Model for tracking status updates on service requests"""
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='status_updates')
    previous_status = models.CharField(max_length=20, choices=ServiceRequest.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=ServiceRequest.STATUS_CHOICES)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='status_updates')
    notes = models.TextField(blank=True, help_text="Notes about this status update (visible to customer)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service_request.request_number} - {self.previous_status} → {self.new_status}"
    
    class Meta:
        verbose_name = "Request Status Update"
        verbose_name_plural = "Request Status Updates"
        ordering = ['-created_at']
