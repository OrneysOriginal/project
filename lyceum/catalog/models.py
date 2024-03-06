import django.core.exceptions
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from catalog.validators import ValidatorArg
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
        unique=True,
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
                {Tag.name.field.name: "есть похожое название"},
            )
        self.normalization_data = normalization_data


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
        upload_to="catalog/mainimage/",
    )
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
    )

    class Meta:
        verbose_name = "Главное изображение"
        verbose_name_plural = "Главное изображение"


class Images(AbstractImage):
    image = django.db.models.ImageField(
        upload_to="catalog/images/",
    )
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"


__all__ = []
