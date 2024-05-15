from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item
from homepage.forms import EchoSubmitForm


def homepage(request):
    template = "homepage/main.html"

    context = {
        "title": "Главная",
        "items": Item.objects.on_main(),
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echoview(request):
    if request.method == "GET":
        template = "homepage/echo_form.html"
        form = EchoSubmitForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, template, context)

    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def plaintext_echo(request):
    if request.method == "POST":
        text = request.POST.get("text")
        context = {
            "form": text,
        }

        template = "homepage/plaintext.html"
        return render(request, template, context)

    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


__all__ = []
