import django.db.models
from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def item_list(request):
    templates = "catalog/item_list.html"
    context = {
        "title": "Список товаров",
        "items": Item.objects.published(),
    }
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "catalog/item.html"
    context = {
        "title": "Товар",
        "item": django.shortcuts.get_object_or_404(
            Item.objects.published(),
            pk=pk,
        ),
    }
    return render(request, templates, context)


def some_re(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


def some_converter(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


__all__ = []
