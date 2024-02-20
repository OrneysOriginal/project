import catalog.models
from django.contrib import admin


@admin.register(catalog.models.CatalogItem)
class AdminItem(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(catalog.models.CatalogTag)
class AdminTag(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("item",)


@admin.register(catalog.models.CatalogCategory)
class AdminCatalogCategory(admin.ModelAdmin):
    list_display = ("name",)
