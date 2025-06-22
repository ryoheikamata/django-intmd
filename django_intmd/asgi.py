import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_intmd.settings.base")

# application = get_asgi_application()
# Initialize django ASGI application before import websocket_urlpatterns in order to avoid circular import.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
    }
)
