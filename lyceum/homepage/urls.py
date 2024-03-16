from django.urls import path

from homepage import views


app_name = "homepage"

urlpatterns = [
    path("", views.homepage, name="main"),
    path("coffee/", views.teapot),
    path("echo/", views.echoview, name="echo_form"),
    path("echo/submit/", views.plaintext_echo, name="echo_plaintext"),
]
