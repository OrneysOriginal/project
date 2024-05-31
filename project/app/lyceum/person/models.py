from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user_id = models.OneToOneField(
        User,
        related_name="profile_id",
        related_query_name="profile_id",
        on_delete=models.CASCADE,
    )
    bio = models.CharField(max_length=255)
    birthday = models.DateField(null=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"


__all__ = [Profile]
