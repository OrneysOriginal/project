from functools import wraps
import re

import django.core.exceptions
from django.core.validators import validate_slug
import django.db.models

from core.models import AbstractCatalog

from lyceum.catalog.validators import validator_take_arg


def minvaluevalidator(num):
    if num <= 0:
        raise django.core.exceptions.ValidationError(
            "Значение ниже или равное 0 недопустимо",
        )


def maxvaluevalidator(num):
    if num > 32767:
        raise django.core.exceptions.ValidationError(
            "Значение выше 32767 недопустимо",
        )


class Category(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text="Напишите слаг(Eng)",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[minvaluevalidator, maxvaluevalidator],
        verbose_name="Вес",
        help_text="Введите вес",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Tag(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text="Напишите слаг(Eng)",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Item(AbstractCatalog):
    text = django.db.models.TextField(
        verbose_name="Текст",
        validators=[validator_take_arg("превосходно", "роскошно")],
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

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
