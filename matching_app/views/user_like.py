from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from matching_app.models import UserLike


@login_required
@require_http_methods(["POST"])
def user_like_toggle(request: HttpRequest, receiver_id: int) -> JsonResponse:
    receiver = get_object_or_404(get_user_model(), id=receiver_id)
    user_like, created = UserLike.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
    )
    like_status = "liked"
    if not created:
        user_like.delete()
        like_status = "unliked"

    return JsonResponse({"like_status": like_status}, status=200)
