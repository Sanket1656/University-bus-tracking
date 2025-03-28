from django.urls import re_path
from .consumers import BusLocationConsumer

websocket_urlpatterns = [
    re_path(r"ws/bus_tracking/$", BusLocationConsumer.as_asgi()),
]

