import re

from core.models import AbstractCatalog
import django.core.exceptions
from django.core.validators import validate_slug
import django.db.models


def words_in_text(text):
    if re.search(r"\bроскошно\b|\bпревосходно\b", text.lower()) is None:
        raise django.core.exceptions.ValidationError(
            "В тексте должно присутсвовать слово 'превосходно' или 'роскошно'"
        )


def minvaluevalidator(num):
    if num <= 0:
        raise django.core.exceptions.ValidationError(
            "Значение ниже или равное 0 недопустимо"
        )


def maxvaluevalidator(num):
    if num > 32767:
        raise django.core.exceptions.ValidationError(
            "Значение выше 32767 недопустимо"
        )


class CatalogCategory(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="Слаг",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[minvaluevalidator, maxvaluevalidator],
        verbose_name="Вес",
    )

    class Meta:
        verbose_name = "категории"
        verbose_name_plural = "категории"


class CatalogTag(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="Слаг",
    )

    class Meta:
        verbose_name = "теги"
        verbose_name_plural = "теги"


class CatalogItem(AbstractCatalog):
    text = django.db.models.TextField(
        verbose_name="Текст",
        validators=[words_in_text],
        help_text="Описание товара",
    )
    category = django.db.models.ForeignKey(
        CatalogCategory,
        on_delete=django.db.models.CASCADE,
        verbose_name="Категории",
        unique=False,
    )
    tags = django.db.models.ManyToManyField(
        CatalogTag, related_name="item", verbose_name="теги"
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товар"
