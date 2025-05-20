from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse  # 正しいインポート文
from django.urls import path


def home(request):
    return HttpResponse("hello world!!!!!!!!!!!!!!!!!!!!")

urlpatterns = (
    [path("home", home, name="home")]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)