"""
WSGI config for gas_utility project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gas_utility.settings')

application = get_wsgi_application()
