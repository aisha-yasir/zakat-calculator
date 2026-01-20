

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zakat_system.settings')

app = get_wsgi_application() # Vercel looks for the name "app"
application = app
