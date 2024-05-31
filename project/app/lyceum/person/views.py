from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import redirect, render, reverse
from django.views import View
from person.forms import LoginForm, RegistrationForm


class ProfilePage(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Профиль",
                "info": User.objects.get(id=self.request.user.id),
            }
            return render(self.request, "user/profile.html", context)

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))


class Login(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            context = {
                "title": "Вход",
                "form": LoginForm,
            }
            return render(self.request, "user/login.html", context)

        messages.error(self.request, "Вы авторизованы")
        return redirect(reverse("homepage:main"))

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = LoginForm(self.request.POST)
            if form.is_valid():
                try:
                    user = User.objects.get(
                        username=self.request.POST.get("username"),
                    )
                except ObjectDoesNotExist:
                    messages.error(self.request, "Такого пользователя нет")
                    return redirect(reverse("person:login"))

                password = self.request.POST.get("password")
                if user.check_password(password):
                    login(self.request, user)

                messages.success(self.request, "Вы авторизованы")
                return redirect(reverse("person:profile"))

        messages.error(self.request, "Вы авторизованы")
        return redirect(reverse("homepage:main"))


class Registration(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            context = {
                "title": "Регистрация",
                "form": RegistrationForm,
            }
            return render(self.request, "user/registration.html", context)

        messages.error(self.request, "Вы авторизованы")
        return redirect(reverse("homepage:main"))

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = RegistrationForm(self.request.POST)
            if form.is_valid():
                try:
                    User.objects.create_user(
                        username=self.request.POST.get("username"),
                        password=self.request.POST.get("password"),
                        email=self.request.POST.get("email"),
                    )
                except IntegrityError:
                    messages.error(
                        self.request,
                        "Пользователь с таким именем уже существует",
                    )
                    return redirect(reverse("person:registration"))

                messages.success(self.request, "Вы зарегистрированы")
                return redirect(reverse("person:profile"))

            messages.success(self.request, "Неверно заполнена форма")
            return redirect(reverse("person:profile"))

        messages.error(self.request, "Вы авторизованы")
        return redirect(reverse("homepage:main"))


class Logout(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, "user/logout.html")

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            return render(self.request, "user/login.html")

        messages.error(self.request, "Вы не авторизованы")
        return redirect(reverse("homepage:main"))


__all__ = []
