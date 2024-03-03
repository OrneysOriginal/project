from django.shortcuts import render


def description(request):
    templates = "about/about.html"
    context = {"title": "О проекте"}
    return render(request, templates, context)


__all__ = []
