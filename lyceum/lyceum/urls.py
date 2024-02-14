from django.contrib import admin
from django.urls import include, path

from . import settings


urlpatterns = [
    path("", include("homepage.urls")),
    path("", include("catalog.urls")),
    path("", include("about.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    from debug_toolbar import urls

    urlpatterns += (path("__debug__/", include(urls)),)
