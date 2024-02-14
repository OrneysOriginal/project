from django.http import HttpResponse


def item_list(request):
    return HttpResponse("Список элементов")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")
