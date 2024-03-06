from http import HTTPStatus

import django.db.models
from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item, Tag


def homepage(request):
    template = "homepage/main.html"

    context = {
        "title": "Главная",
        "items": Item.objects.filter(is_on_main=True)
        .select_related("category")
        .select_related("main_image")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=Tag.objects.filter(is_published=True).only("name"),
            ),
        )
        .only("category__name", "tags__name", "text", "name")
        .filter(category__is_published=True),
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = []
