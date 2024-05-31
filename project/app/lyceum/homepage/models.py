from django.db.models import Model, TextField


class EchoSubmit(Model):
    text = TextField(
        verbose_name="текст",
    )


__all__ = []
