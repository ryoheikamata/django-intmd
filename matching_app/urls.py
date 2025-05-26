from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # 正しいインポート文
from django.urls import path

from matching_app.views.signup import signup # 追加
from matching_app.views.user_profile import user_home # 追加

urlpatterns = (
    [
         # Auth
         path("signup/", signup, name="signup"),  # 追加
             # User profile
         path("home/", user_home, name="user_home"),  # 追加
     ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)