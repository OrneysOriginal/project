from django.urls import path, re_path, register_converter

from catalog import converter, views


register_converter(converter.IntPLusDig, "positive")
app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(r"^re/(?P<pk>[1-9]\d*)/$", views.some_re),
    path("converter/<positive:pk>/", views.some_converter),
]
