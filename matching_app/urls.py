from django.urls import path
from django.http import HttpResponse  # 正しいインポート文

def home(request):
    return HttpResponse('hello world!!!!!!!!!!!!!!!!!!!!')

urlpatterns = [
    path('home', home, name='home')
]
