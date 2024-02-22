import re

import django.core.exceptions
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidatorArg:

    def __init__(self, word1, word2, num=1):
        regular_left = r"\b" + word1 + r"\b"
        regular_right = r"\b" + word2 + r"\b"
        self.regular = regular_left + "|" + regular_right
        self.num = num

    def __call__(self, text):
        if re.search(self.regular, text.lower()) is None:
            raise django.core.exceptions.ValidationError(
                "В тексте должно присутсвовать слово"
                " 'превосходно' или 'роскошно'",
            )

    def __eq__(self, other):
        return self.num == other.num


class ValidatorSerializer(BaseSerializer):
    def serialize(self):
        return repr(self.value), {"from validators import ValidatorArg"}


MigrationWriter.register_serializer(ValidatorArg, ValidatorSerializer)
