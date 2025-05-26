from django.contrib.auth import get_user_model
from django.db import models

from matching_app.models.base import BaseModel


class UserVerification(BaseModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
