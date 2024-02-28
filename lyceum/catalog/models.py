import re

import django.core.exceptions
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from sorl.thumbnail import get_thumbnail
from unidecode import unidecode

from catalog.validators import ValidatorArg
from core.models import AbstractCatalog


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return unidecode("".join(words))


class Category(AbstractCatalog):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="Напишите слаг(Eng)",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
        verbose_name="вес",
        help_text="Введите вес",
    )
    normalization_data = django.db.models.CharField(
        max_length=150,
        verbose_name="правильные данные",
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def clean(self):
        normalization_data = normalize_str(self.name)
        found = Category.objects.filter(
            normalization_data=normalization_data,
        )
        if found and found[0] != self:
            raise django.core.exceptions.ValidationError(
                {Category.name.field.name: "есть похожое название"},
            )
        self.normalization_data = normalization_data


class Tag(AbstractCatalog):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="Напишите слаг(Eng)",
    )
    normalization_data = django.db.models.CharField(
        max_length=150,
        verbose_name="правильные данные",
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def clean(self):
        normalization_data = normalize_str(self.name)
        found = Tag.objects.filter(
            normalization_data=normalization_data,
        )
        if found and found[0] != self:
            raise django.core.exceptions.ValidationError(
                {Tag.name.field.name: "есть похожое название"},
            )
        self.normalization_data = normalization_data


class MainImage(models.Model):
    image = models.ImageField(
        upload_to="",
        verbose_name="главное изображение",
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

    class Meta:
        verbose_name = "Главное изображение"
        verbose_name_plural = "Главное изображение"


class Images(models.Model):
    image = models.ImageField(
        upload_to="",
        verbose_name="картинки",
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

    class Meta:
        verbose_name = "Картинки"
        verbose_name_plural = "Картинки"


class Item(AbstractCatalog):
    text = django.db.models.TextField(
        verbose_name="текст",
        validators=[ValidatorArg("превосходно", "роскошно")],
        help_text="Описание товара",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категории",
        unique=False,
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="item",
        verbose_name="теги",
    )
    images = django.db.models.ForeignKey(
        Images,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        null=False,
        verbose_name="Изображения",
    )
    main_image = django.db.models.OneToOneField(
        to=MainImage,
        on_delete=django.db.models.CASCADE,
        null=False,
        verbose_name="Главное изображение",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


__all__ = ["Category", "Tag", "MainImage", "Images", "Item"]
