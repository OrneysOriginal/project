class IntPLusDig:
    regex = r"[1-9]\d*"

    def to_python(self, positive):
        return int(positive)

    def to_url(self, positive):
        return str(positive)


__all__ = []
