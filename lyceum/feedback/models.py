from django.core.validators import EmailValidator
import django.db.models
from django.db.models import Model


class Feedback(Model):
    text = django.db.models.TextField(
        verbose_name="текст",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
    )
    mail = django.db.models.EmailField(
        verbose_name="email",
        max_length=100,
        validators=[EmailValidator],
    )


__all__ = []
