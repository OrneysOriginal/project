from functools import wraps
import re

import django.core.exceptions


def validator_take_arg(word1, word2):
    regular_left = r"\b" + word1 + r"\b"
    regular_right = r"\b" + word2 + r"\b"
    regular = regular_left + "|" + regular_right

    @wraps(validator_take_arg)
    def validator(text):
        if re.search(regular, text.lower()) is None:
            raise django.core.exceptions.ValidationError(
                "В тексте должно присутсвовать слово"
                " 'превосходно' или 'роскошно'",
            )

    return validator
