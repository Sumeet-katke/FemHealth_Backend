import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femhealth.settings')
django.setup()

# django.setup(


from fembot.chatbot_engines.routing import websocket_urlpatterns  # You'll create this
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from fembot.middleware import JWTAuthMiddleware
# import fembot.routing  # Where your WebSocket URL is defined

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Default for HTTP requests
    "websocket": JWTAuthMiddleware(  # WebSocket route with JWT middleware
        URLRouter(
            websocket_urlpatterns
        )
    ),
})