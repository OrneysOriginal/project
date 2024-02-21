import catalog.models
from django.contrib import admin


@admin.register(catalog.models.Item)
class AdminItem(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(catalog.models.Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    filter_horizontal = ("item",)


@admin.register(catalog.models.Category)
class AdminCatalogCategory(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
