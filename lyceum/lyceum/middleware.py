import re

from django.conf import settings


class ReverseRusWordMiddleware:
    count = 1

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def change_count(cls):
        if cls.count == 10:
            cls.count = 1
        else:
            cls.count += 1

    def __call__(self, request):
        response = self.get_response(request)
        if ReverseRusWordMiddleware.count == 10:
            if settings.ALLOW_REVERSE:
                text = response.content.decode("utf-8")
                words = re.findall("[а-яА-ЯёЁ]+", text)
                rus_reverse_words = {}
                for i in range(len(words)):
                    rus_reverse_words[words[i]] = words[i][::-1]

                strip_text = text.strip("<body>").strip("</>").split()
                for i in range(len(strip_text)):
                    if rus_reverse_words.get(strip_text[i]) is not None:
                        strip_text[i] = rus_reverse_words[strip_text[i]]

                text = " ".join(strip_text)
                response.content = text.encode("utf-8")

        self.change_count()
        return response


__all__ = []
