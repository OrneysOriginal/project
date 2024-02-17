from django.contrib import admin
from django.urls import path
from homepage import views


urlpatterns = [
    path("", views.homepage),
    path("coffee/", views.teapot),
    path("admin/", admin.site.urls),
]
