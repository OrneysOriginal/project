from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import MainImage


def homepage(request):
    template = "homepage/main.html"

    context = {
        "title": "Главная",
        "mainimage": MainImage.objects.filter()[:6],
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = []
