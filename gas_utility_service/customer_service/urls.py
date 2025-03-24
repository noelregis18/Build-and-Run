from django.urls import path
from . import views

urlpatterns = [
    # Customer facing URLs
    path('requests/', views.request_list, name='request_list'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<str:request_number>/', views.request_detail, name='request_detail'),
    
    # Support staff URLs
    path('support/dashboard/', views.support_dashboard, name='support_dashboard'),
    path('support/requests/<str:request_number>/', views.support_request_detail, name='support_request_detail'),
    path('support/requests/<str:request_number>/update/', views.update_request, name='update_request'),
]
