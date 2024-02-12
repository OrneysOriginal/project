from django.http import HttpResponse


def homepage(request):
    return HttpResponse("<body>Главная</body>")
