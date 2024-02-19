from django.db import models


class AbstractCatalog(models.Model):
    id = models.IntegerField(primary_key=True, name="id")
    name = models.CharField(max_length=150, name="Название")
    is_published = models.BooleanField(default=True, name="Опубликовано")

    def __str__(self):
        return self.name
