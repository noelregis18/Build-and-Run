from django.contrib import admin
from .models import ServiceRequest, ServiceType, RequestAttachment, RequestStatusUpdate

# Register service types
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

# Inline for attachments
class RequestAttachmentInline(admin.TabularInline):
    model = RequestAttachment
    extra = 0

# Inline for status updates
class RequestStatusUpdateInline(admin.TabularInline):
    model = RequestStatusUpdate
    extra = 0
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

# Register service requests
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'customer', 'service_type', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('request_number', 'customer__username', 'customer__email', 'description')
    readonly_fields = ('request_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [RequestAttachmentInline, RequestStatusUpdateInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('request_number', 'customer', 'service_type')
        }),
        ('Request Details', {
            'fields': ('description', 'status', 'priority')
        }),
        ('Support Staff Assignment', {
            'fields': ('assigned_to', 'support_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # Only show active users in the assigned_to dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(is_staff=True, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Import needed for the assigned_to queryset modification
from django.contrib.auth.models import User
