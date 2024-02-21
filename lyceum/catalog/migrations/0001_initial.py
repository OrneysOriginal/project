# Generated by Django 4.2 on 2024-02-21 13:29

import catalog.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите навзание",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="выберите будет ли опубликовано",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="Напишите слаг(Eng)",
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                        verbose_name="слаг",
                    ),
                ),
                (
                    "weight",
                    models.IntegerField(
                        default=100,
                        help_text="Введите вес",
                        validators=[
                            catalog.models.minvaluevalidator,
                            catalog.models.maxvaluevalidator,
                        ],
                        verbose_name="Вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите навзание",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="выберите будет ли опубликовано",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="Напишите слаг(Eng)",
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                        verbose_name="слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите навзание",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="выберите будет ли опубликовано",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Описание товара",
                        validators=[catalog.models.words_in_text],
                        verbose_name="Текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                        verbose_name="категории",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        related_name="item",
                        to="catalog.tag",
                        verbose_name="теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
