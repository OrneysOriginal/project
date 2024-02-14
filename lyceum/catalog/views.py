from django.http import HttpResponse


def item_list(request):
    return HttpResponse(b"\\xd0\\xa1\\xd0\\xbf\\xd0\\xb8"
                        b"\\xd1\\x81\\xd0\\xbe\\xd0\\xba \\xd1\\x8d\\xd0"
                        b"\\xbb\\xd0\\xb5\\xd0\\xbc\\xd0"
                        b"\\xb5\\xd0\\xbd\\xd1\\x82\\xd0\\xbe\\xd0\\xb2")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")
