from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item, MainImage


def item_list(request):
    templates = "catalog/item_list.html"
    context = {
        "title": "Список товаров",
        "mainimage": MainImage.objects.filter(),
        "MainImage": MainImage,
    }
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "catalog/item.html"
    context = {
        "title": "Товар",
        "item": [x.main_image for x in Item.objects.filter(id=pk)],
    }
    return render(request, templates, context)


def some_re(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


def some_converter(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


__all__ = []
