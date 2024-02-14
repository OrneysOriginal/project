from django.urls import path

from catalog import views


urlpatterns = [
    path("catalog/", views.item_list),
<<<<<<< HEAD
    path("catalog/<int:pk>/", views.item_detail),
=======
    path("catalog/<int:pk>", views.item_detail),
>>>>>>> 27e6800dcca08483e025bac5de6ea55f82d0e126
]
