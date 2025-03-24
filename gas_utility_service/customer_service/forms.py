from django import forms
from .models import ServiceRequest, RequestAttachment, RequestStatusUpdate

class ServiceRequestForm(forms.ModelForm):
    """Form for creating new service requests"""
    # Django's standard forms don't support multiple file uploads in widgets
    # We'll handle multiple uploads manually in the view using request.FILES
    attachments = forms.FileField(required=False)
    
    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please describe your request in detail'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class RequestStatusUpdateForm(forms.ModelForm):
    """Form for updating request status (for support staff)"""
    class Meta:
        model = RequestStatusUpdate
        fields = ['new_status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.service_request = kwargs.pop('service_request', None)
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SupportRequestUpdateForm(forms.ModelForm):
    """Form for support staff to update service requests"""
    class Meta:
        model = ServiceRequest
        fields = ['status', 'priority', 'assigned_to', 'support_notes']
        widgets = {
            'support_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
