"""
WSGI config for Yoga project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yoga.settings')
sys.path.append('/var/www/cydez-yoga/Yoga')
sys.path.append('/var/www/cydez-yoga/Yoga/Yoga')
application = get_wsgi_application()
