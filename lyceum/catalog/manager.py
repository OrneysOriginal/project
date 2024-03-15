import importlib

import django


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .select_related("category")
            .select_related("main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=importlib.import_module("catalog.models")
                    .Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only("category__name", "tags__name", "text", "name")
            .filter(category__is_published=True)
        ).filter(is_published=True)

    def on_main(self):
        return self.published().filter(is_on_main=True)