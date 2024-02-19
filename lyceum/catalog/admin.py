from django.contrib import admin

import catalog.models


@admin.register(catalog.models.CatalogItem)
class AdminItem(admin.ModelAdmin):
    list_display = (
        'Текст',
        'Опубликовано',
        'Название',
    )
    list_display_links = (
        'Текст',
    )
    list_editable = (
        'Название',
    )


@admin.register(catalog.models.CatalogTag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        'Название',
    )
    filter_horizontal = ('item',)


@admin.register(catalog.models.CatalogCategory)
class AdminCatalogCategory(admin.ModelAdmin):
    list_display = (
        'Название',
        'Слаг',
        'Вес',
    )
