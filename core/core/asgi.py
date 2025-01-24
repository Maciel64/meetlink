"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from meetlink.domain.call.call_consumer import CallConsumer
from meetlink.domain.meeting.meeting_consumer import MeetingConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    re_path("ws/calls/?$", CallConsumer.as_asgi()),
                    re_path("ws/meetings/?$", MeetingConsumer.as_asgi()),
                ]
            )
        ),
    }
)
