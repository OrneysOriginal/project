import re

from django.db import models
from sorl.thumbnail import get_thumbnail
from unidecode import unidecode


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return unidecode("".join(words))


class AbstractCatalog(models.Model):
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


class AbstractImage(models.Model):
    image = models.ImageField(
        upload_to="",
    )

    def get_image300x300(self):
        return get_thumbnail(self.image, "300x300", crop="center", quality=51)

    def image_tmb(self):
        if self.image:
            im = get_thumbnail(
                self.image,
                "300x300",
                crop="center",
                quality=51,
            )
            return im
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


__all__ = ["AbstractCatalog"]
