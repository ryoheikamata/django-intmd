from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse # HttpResponseを追加
from django.shortcuts import get_object_or_404, render # renderを追加
from django.views.decorators.http import require_http_methods
from matching_app.models import UserLike

@login_required
@require_http_methods(["GET"])
def user_like_list(request: HttpRequest) -> HttpResponse:
    sent_user_likes = UserLike.objects.filter(sender=request.user).select_related("receiver")
    received_user_likes = UserLike.objects.filter(receiver=request.user).select_related("sender")

    all_receivers = [user_like.receiver for user_like in sent_user_likes]
    all_senders = [user_like.sender for user_like in received_user_likes]
    matched_users = list(set(all_receivers) & set(all_senders))

    receivers = [user for user in all_receivers if user not in matched_users]
    senders = [user for user in all_senders if user not in matched_users]

    return render(
        request,
        "user_like_list.html",
        {
            "matched_users": matched_users,
            "receivers": receivers,
            "senders": senders,
        },
    )
