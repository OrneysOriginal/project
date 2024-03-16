from http import HTTPStatus

from django.http import Http404, HttpResponse
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
    template = "homepage/echo_form.html"
    form = EchoSubmitForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, template, context)


def plaintext_echo(request):
    if request.method == "POST":
        text = request.POST.get("text")
        context = {
            "form": text,
        }
        template = "homepage/plaintext.html"
        return render(request, template, context)
    raise Http404()


__all__ = []
