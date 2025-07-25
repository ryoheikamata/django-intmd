from django.urls import re_path

from matching_app.channels.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<room_id>\d+)/$", ChatConsumer.as_asgi()),
]