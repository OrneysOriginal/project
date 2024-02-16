from catalog import converter, views
from django.urls import path, re_path, register_converter


register_converter(converter.IntPLusDig, "value")

urlpatterns = [
    path("catalog/", views.item_list),
    path("catalog/<int:pk>/", views.item_detail),
    re_path(r"^catalog/re/(?P<pk>[1-9]\d*)/$", views.some_re),
    path("catalog/converter/<value:pk>/", views.some_converter),
]
