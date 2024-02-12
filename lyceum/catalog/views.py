from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Cписок элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")
