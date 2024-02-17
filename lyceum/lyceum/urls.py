from django.urls import include, path


urlpatterns = [
    path("", include("homepage.urls")),
    path("", include("catalog.urls")),
    path("", include("about.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
