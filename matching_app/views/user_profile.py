from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def user_home(request: HttpRequest) -> HttpResponse:
    return render(request, "user_home.html", {"user": request.user, "user_profile": request.user.userprofile})
