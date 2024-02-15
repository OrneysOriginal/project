from django.http import HttpResponse


def homepage(request):
    return HttpResponse("<body>Главная</body>")


def teapot(request):
    return HttpResponse(content="<body>Я чайник</body>", status=418)
