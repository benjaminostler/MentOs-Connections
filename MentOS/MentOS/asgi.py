"""
ASGI config for MentOS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import MentOS_app.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MentOS.settings')

application = ProtocolTypeRouter ({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            MentOS_app.routing.websocket_urlpatterns
        )
    ), 
})

