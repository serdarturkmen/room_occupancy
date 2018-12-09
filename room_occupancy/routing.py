from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from rooms.consumers import Consumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/", Consumer),
    ])
})
