from django.apps import AppConfig


class HomepageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = "Домашняя страница"


__all__ = ["HomepageConfig"]
