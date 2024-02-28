from django.db import models


class AbstractCatalog(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="id",
    )
    name = models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="Введите навзание",
        unique=True,
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="выберите будет ли опубликовано",
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        abstract = True


__all__ = ["AbstractCatalog"]
