from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def some_re(request, pk):
    return HttpResponse(f"<body>{pk}</body>")


def some_converter(request, pk):
    return HttpResponse(f"<body>{pk}</body>")
