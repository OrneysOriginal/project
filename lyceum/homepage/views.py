from django.http import HttpResponse


def homepage(request):
    return HttpResponse("<body>Главная</body>")


def teapot(request):
    return HttpResponse(content="Я чайник", status=418)
