from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ServiceType, ServiceRequest
from accounts.models import CustomerProfile

class CustomerServiceTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Create customer profile
        self.profile = CustomerProfile.objects.create(
            user=self.user,
            account_number='TEST12345',
            address='123 Test Street, Test City',
            phone_number='555-1234'
        )
        
        # Create service type
        self.service_type = ServiceType.objects.create(
            name='Gas Leak',
            description='Report a gas leak',
            is_active=True
        )
        
        # Create service request
        self.service_request = ServiceRequest.objects.create(
            customer=self.user,
            service_type=self.service_type,
            description='I smell gas in my kitchen',
            status='pending',
            priority='high'
        )
    
    def test_request_list_view(self):
        """Test the request list view for authenticated users"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.request_number)
    
    def test_request_detail_view(self):
        """Test the request detail view for authenticated users"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('request_detail', args=[self.service_request.request_number]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'I smell gas in my kitchen')
