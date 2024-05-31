from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import django.db.models
from django.shortcuts import redirect, render, reverse
from django.views import View

from catalog.models import Basket, Item


class ItemList(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            templates = "catalog/item_list.html"
            context = {
                "title": "Список товаров",
                "items": Item.objects.published(),
            }
            return render(self.request, templates, context)

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))


class ItemDetail(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            templates = "catalog/item.html"
            context = {
                "title": "Товар",
                "item": django.shortcuts.get_object_or_404(
                    Item.objects.published(),
                    pk=kwargs.get("pk"),
                ),
            }
            return render(self.request, templates, context)

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                Basket.objects.get(
                    user_id=self.request.user.id,
                    item_id=kwargs.get("pk"),
                )
            except ObjectDoesNotExist:
                Basket.objects.create(
                    user_id=self.request.user.id,
                    item_id=kwargs.get("pk"),
                )
                messages.success(
                    self.request, "Товар успешно добавлен в вашу корзину",
                )
                return redirect(reverse("catalog:item_list"))
            else:
                messages.info(self.request, "Товар уже в вашей корзине")
                return redirect(reverse("catalog:item_list"))

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))


class BasketView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            items = Basket.objects.filter(user_id=self.request.user.id)
            context = {
                "title": "Корзина",
                "basket": items,
                "length": len(items),
            }
            return render(self.request, "user/basket.html", context)

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            pass

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))


__all__ = []
