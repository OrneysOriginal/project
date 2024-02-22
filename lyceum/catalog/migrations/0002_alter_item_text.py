# Generated by Django 4.2 on 2024-02-22 19:24

import catalog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Описание товара",
                validators=[catalog.validators.ValidatorArg],
                verbose_name="Текст",
            ),
        ),
    ]
