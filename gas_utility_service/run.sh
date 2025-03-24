#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Create necessary directories if they don't exist
mkdir -p media/request_attachments

# Apply database migrations
echo "Making migrations for accounts app..."
python manage.py makemigrations accounts
echo "Making migrations for customer_service app..."
python manage.py makemigrations customer_service
echo "Applying all migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Create service types if they don't exist
echo "from customer_service.models import ServiceType; ServiceType.objects.get_or_create(name='Gas Leak', description='Report a suspected gas leak or gas odor', is_active=True); ServiceType.objects.get_or_create(name='Billing Question', description='Questions about your gas bill or payment', is_active=True); ServiceType.objects.get_or_create(name='New Service', description='Request new gas service for your property', is_active=True); ServiceType.objects.get_or_create(name='Service Transfer', description='Transfer your gas service to a new address', is_active=True); ServiceType.objects.get_or_create(name='Service Termination', description='Request to terminate your gas service', is_active=True); ServiceType.objects.get_or_create(name='Meter Reading', description='Request a meter reading or report a meter issue', is_active=True); ServiceType.objects.get_or_create(name='Gas Appliance Issue', description='Problems with gas appliances or equipment', is_active=True); ServiceType.objects.get_or_create(name='Other', description='Other requests not listed above', is_active=True);" | python manage.py shell

# Run the development server
echo "Starting server at http://0.0.0.0:5000/"
python manage.py runserver 0.0.0.0:5000
