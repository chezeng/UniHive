"""
<<<<<<<< HEAD:Backend/myproject/wsgi.py
WSGI config for myproject project.
========
WSGI config for forum project.
>>>>>>>> 8c3262cd4e45c1375935d2c68241cea141afc0a4:Backend/forum/wsgi.py

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<<< HEAD:Backend/myproject/wsgi.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum.settings')
>>>>>>>> 8c3262cd4e45c1375935d2c68241cea141afc0a4:Backend/forum/wsgi.py

application = get_wsgi_application()
