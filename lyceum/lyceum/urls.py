from django.contrib import admin
from django.urls import include, path

from . import settings


urlpatterns = [
    path("", include("homepage.urls")),
    path("", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    from lyceum import INSTALLED_APPS, MIDDLEWARE

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
