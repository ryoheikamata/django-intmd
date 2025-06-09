from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # 正しいインポート文
from django.urls import path

from matching_app.views.index import index
from matching_app.views.login import login_view, logout_view
from matching_app.views.signup import signup
from matching_app.views.user_profile import user_home
from matching_app.views.verify import send_new_verification_code, verify_email # 追加

urlpatterns = (
    [
        # Index
        path("", index, name="index"),  # 追加
         # Auth
        path("signup/", signup, name="signup"),  # 追加
        path("signup/verify/<int:id>/", verify_email, name="verify_email"),  # 追加
        path("signup/verify/resend/<int:id>/", send_new_verification_code, name="send_new_verification_code"),  # 追加
        path("login/", login_view, name="login"),  # 追加
        path("logout/", logout_view, name="logout"),  # 追加
        # User profile
         path("home/", user_home, name="user_home"),  # 追加
     ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)