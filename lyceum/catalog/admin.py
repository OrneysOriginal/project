from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Item)
class AdminItem(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.main_image.field.name,
        catalog.models.Item.images.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)


@admin.register(catalog.models.Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)


@admin.register(catalog.models.Category)
class AdminCatalogCategory(admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )
    list_editable = (catalog.models.Category.is_published.field.name,)


@admin.register(catalog.models.MainImage)
class AdminMainImage(admin.ModelAdmin):
    list_display = [
        catalog.models.MainImage.image_tmb,
        catalog.models.MainImage.get_image300x300,
    ]


@admin.register(catalog.models.Images)
class AdminImages(admin.ModelAdmin):
    list_display = [
        catalog.models.Images.image.field.name,
    ]


__all__ = []
