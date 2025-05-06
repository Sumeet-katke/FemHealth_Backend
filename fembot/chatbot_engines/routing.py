from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chatbot/', consumers.ChatBotConsumer.as_asgi()),  # Remove the `$` here
]
