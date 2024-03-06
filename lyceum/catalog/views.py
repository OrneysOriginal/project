import django.db.models
from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item, Tag


def item_list(request):
    templates = "catalog/item_list.html"
    context = {
        "title": "Список товаров",
        "items": Item.objects.filter(is_published=True)
        .select_related("category")
        .select_related("main_image")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            ),
        )
        .only("category__name", "tags__name", "text", "name")
        .filter(category__is_published=True)
        .order_by("category__name"),
    }
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "catalog/item.html"
    context = {
        "title": "Товар",
        "item": django.shortcuts.get_object_or_404(
            Item.objects.filter(is_published=True),
            pk=pk,
        ),
    }
    return render(request, templates, context)


def some_re(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


def some_converter(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


__all__ = []
