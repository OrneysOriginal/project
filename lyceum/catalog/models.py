import re

import django.core.exceptions
from django.core.validators import validate_slug
import django.db.models
from unidecode import unidecode

from catalog.validators import ValidatorArg
from core.models import AbstractCatalog


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return unidecode("".join(words))


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
    normalization_data = django.db.models.CharField(
        max_length=150,
        verbose_name="Правильные данные",
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def clean(self):
        normalization_data = normalize_str(self.name)
        found = self.__class__.objects.filter(
            normalization_data=normalization_data,
        )
        if found and found[0] != self:
            raise django.core.exceptions.ValidationError(
                {self.__class__.name.field.name: "есть похожое название"},
            )
        self.normalization_data = normalization_data


class Tag(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text="Напишите слаг(Eng)",
    )
    normalization_data = django.db.models.CharField(
        max_length=150,
        verbose_name="Правильные данные",
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def clean(self):
        normalization_data = normalize_str(self.name)
        found = self.__class__.objects.filter(
            normalization_data=normalization_data,
        )
        if found and found[0] != self:
            raise django.core.exceptions.ValidationError(
                {self.__class__.name.field.name: "есть похожое название"},
            )
        self.normalization_data = normalization_data


class Item(AbstractCatalog):
    text = django.db.models.TextField(
        verbose_name="Текст",
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

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
