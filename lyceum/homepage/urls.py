from django.urls import path

from homepage import views


urlpatterns = [
    path("", views.homepage, name="main"),
    path("coffee/", views.teapot),
]
