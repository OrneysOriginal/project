from django.db import models


class AbstractCatalog(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    name = models.CharField(max_length=150, verbose_name="Название")
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликовано"
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
