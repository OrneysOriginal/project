class IntPLusDig:
    regex = r"[1-9]\d*"

    def to_python(self, id):
        return int(id)

    def to_url(self, id):
        return id
