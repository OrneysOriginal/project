from django.urls import path, register_converter

from catalog import converter, views


register_converter(converter.IntPLusDig, "positive")
app_name = "catalog"

urlpatterns = [
    path("", views.ItemList.as_view(), name="item_list"),
    path("<int:pk>/", views.ItemDetail.as_view(), name="item_detail"),
    path("basket/", views.BasketView.as_view(), name="basket"),
]
