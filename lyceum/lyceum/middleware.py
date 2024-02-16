import re

from django.conf import settings


count = 1


class ReverseRusWord:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global count
        response = self.get_response(request)
        count += 1
        if count == 10:
            if settings.ALLOW_REVERSE:
                count = 1
                text = response.content.decode("utf-8")
                words = re.findall("[а-яА-ЯёЁ]+", text)
                for i in range(len(words)):
                    text = text.replace(words[i], words[i][::-1])
                response.content = text.encode("utf-8")
        return response
