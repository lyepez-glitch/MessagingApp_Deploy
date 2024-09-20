from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from messaging.consumers import MessageConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/some_path/', MessageConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
