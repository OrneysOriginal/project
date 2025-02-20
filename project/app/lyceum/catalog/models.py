import importlib

from django.contrib.auth.models import User
import django.core.exceptions
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from core.models import AbstractCatalog, AbstractImage, normalize_str


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
        editable=False,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def clean(self):
        normalization_data = normalize_str(self.name)
        if Category.objects.filter(
            normalization_data=normalization_data,
        ).exists():
            raise django.core.exceptions.ValidationError(
                {Category.name.field.name: "есть похожее название"},
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
        editable=False,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def clean(self):
        normalization_data = normalize_str(self.name)
        if Category.objects.filter(
            normalization_data=normalization_data,
        ).exists():
            raise django.core.exceptions.ValidationError(
                {Tag.name.field.name: "есть похожее название"},
            )

        self.normalization_data = normalization_data


class ItemManager(django.db.models.Manager):
    def published(self):
        selects = (
            self.get_queryset()
            .select_related("category")
            .select_related("main_image")
        )
        prefetch_inner = django.db.models.Prefetch(
            "tags",
            queryset=importlib.import_module("catalog.models")
            .Tag.objects.filter(is_published=True)
            .only(
                "name",
            ),
        )
        return (
            selects.prefetch_related(
                prefetch_inner,
            )
            .only("category__name", "tags__name", "text", "name")
            .filter(category__is_published=True)
        ).filter(is_published=True)

    def on_main(self):
        return self.published().filter(is_on_main=True)


class Item(AbstractCatalog):
    objects = ItemManager()
    text = django.db.models.TextField(
        verbose_name="текст",
        help_text="Описание товара",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категории",
        unique=False,
        help_text="Выберите категорию",
        related_name="item",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_query_name="items",
        related_name="item",
        verbose_name="теги",
    )
    is_on_main = django.db.models.BooleanField(
        default=False,
    )

    def get_image(self):
        image = MainImage.objects.filter(item_id=self.id)[0]
        return mark_safe(f"<img src='{image.get_image300x300().url}'>")

    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"


class MainImage(AbstractImage):
    image = django.db.models.ImageField(
        upload_to="catalog/mainimage/%Y/%m/%d",
    )
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
    )

    class Meta:
        verbose_name = "Главное изображение"
        verbose_name_plural = "Главное изображение"


class Images(AbstractImage):
    image = django.db.models.ImageField(
        upload_to="catalog/images/%Y/%m/%d",
    )
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"


class Basket(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        unique=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


__all__ = []
