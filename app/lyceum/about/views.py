from django.db.models.query import QuerySet
from django.shortcuts import render


def description(request):
    templates = "about/about.html"
    context = {
        "title": "О проекте",
        "items": QuerySet,
    }
    return render(request, templates, context)


__all__ = []
