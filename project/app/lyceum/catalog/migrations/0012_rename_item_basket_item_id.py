# Generated by Django 4.2 on 2024-05-31 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0011_alter_item_text"),
    ]

    operations = [
        migrations.RenameField(
            model_name="basket",
            old_name="item",
            new_name="item_id",
        ),
    ]
