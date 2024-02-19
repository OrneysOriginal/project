from core.models import AbstractCatalog
import django.db.models
import django.core.exceptions
from django.core.validators import validate_slug


def words_in_text(text):
    if not('превосходно' in text or 'роскошно' in text):
        raise django.core.exceptions.ValidationError(
            'В тексте должно быть "роскошно" или "превосходно"'
        )


def minvaluevalidator(num):
    if num >= 0:
        pass
    else:
        raise django.core.exceptions.ValidationError(
            'Значение ниже 0 недопустимо'
        )


def maxvaluevalidator(num):
    if num > 32767:
        raise django.core.exceptions.ValidationError(
            'Значение выше 32767 недопустимо'
        )


class CatalogCategory(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        name='Слаг'
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            minvaluevalidator,
            maxvaluevalidator
        ],
        name='Вес'
    )

    class Meta:
        verbose_name = 'категория'


class CatalogItem(AbstractCatalog):
    text = django.db.models.TextField(
        name='Текст',
        validators=[words_in_text]
    )
    category = django.db.models.OneToOneField(
        CatalogCategory,
        on_delete=django.db.models.CASCADE,
        default='овощи',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товар'


class CatalogTag(AbstractCatalog):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        name='Слаг'
    )
    item = django.db.models.ManyToManyField(CatalogItem)

    class Meta:
        verbose_name = 'тег'
