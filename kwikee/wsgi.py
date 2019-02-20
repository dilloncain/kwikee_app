"""
WSGI config for kwikee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kwikee.settings")

application = get_wsgi_application()

# whitenoise package is being used to serve static files on Heroku
from whitenoise.django import DjangoWhiteNoise                      # Reason for importing
application = DjangoWhiteNoise(application)                         # Pass application into DjangoWhiteNoise
