import django.core.exceptions
from django.core.validators import MaxValueValidator, MinValueValidator

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

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class MainImage(AbstractImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
    )

    class Meta:
        verbose_name = "Главное изображение"
        verbose_name_plural = "Главное изображение"


class Images(AbstractImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"


__all__ = ["Category", "Tag", "MainImage", "Images", "Item"]
