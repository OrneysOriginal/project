import re

import django.core.exceptions
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidatorArg:

    def __init__(self, *args, num=1):
        self.arg = args
        self.regular = r"\b" + args[0] + r"\b"
        for i in range(1, len(args)):
            self.regular += r"|\b" + args[i] + r"\b"
        self.num = num

    def __call__(self, text):
        if re.search(self.regular, text.lower()) is None:
            raise django.core.exceptions.ValidationError(
                "В тексте должно присутсвовать хотя бы одно из слов"
                f"{self.arg}",
            )

    def __eq__(self, other):
        return self.num == other.num


class ValidatorSerializer(BaseSerializer):
    def serialize(self):
        return repr(self.value), {"from validators import ValidatorArg"}


MigrationWriter.register_serializer(ValidatorArg, ValidatorSerializer)


__all__ = []
