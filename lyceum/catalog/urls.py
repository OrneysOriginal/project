from catalog import converter, views
from django.urls import path, re_path, register_converter


register_converter(converter.IntPLusDig, "value")

urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    re_path(r"^re/(?P<pk>[1-9]\d*)/$", views.some_re),
    path("converter/<value:pk>/", views.some_converter),
]
