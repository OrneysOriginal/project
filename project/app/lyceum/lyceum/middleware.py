import re

import django.conf


WORDS_REGEX = re.compile(r"\w+|\W+")
RUSSIAN_REGEX = re.compile(r"^[а-яА-ЯёЁ]+$")


class ReverseRusWordMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not django.conf.settings.ALLOW_REVERSE:
            return False

        cls.count += 1
        if cls.count != 10:
            return False

        cls.count = 0
        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        content = response.content.decode()
        words = WORDS_REGEX.findall(content)

        transformed = [
            word[::-1] if RUSSIAN_REGEX.search(word) else word
            for word in words
        ]

        response.content = "".join(transformed).encode()
        return response


__all__ = []
