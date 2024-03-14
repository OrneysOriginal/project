from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def homepage(request):
    template = "homepage/main.html"

    context = {
        "title": "Главная",
        "items": Item.objects.on_main(),
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = []
