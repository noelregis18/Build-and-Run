from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CustomerProfile

class AccountsTestCase(TestCase):
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
    
    def test_login_view(self):
        """Test the login functionality"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login
        
    def test_profile_view(self):
        """Test the profile view for authenticated users"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST12345')  # Account number should be on page
