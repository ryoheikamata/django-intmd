from django.http import HttpResponse  # 正しいインポート文
from django.urls import path


def home(request):
    return HttpResponse("hello world!!!!!!!!!!!!!!!!!!!!")


urlpatterns = [path("home", home, name="home")]
