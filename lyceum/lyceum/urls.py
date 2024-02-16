from django.contrib import admin
from django.urls import include, path
from lyceum import settings


urlpatterns = [
    path("", include("homepage.urls")),
    path("", include("catalog.urls")),
    path("", include("about.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
