from catalog import views

from django.urls import path


urlpatterns = [
    path("catalog/", views.item_list),
    path("catalog/<int:pk>/", views.item_detail),
    path("catalog/<int:pk>", views.item_detail),
]
