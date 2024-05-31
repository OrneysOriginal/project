from django import forms
from django.core.validators import validate_slug


class BootsTrap(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widjet.attrs["class"] = "form-label"


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label="Имя пользователя")
    password = forms.CharField(max_length=255, label="Пароль")


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        validators=[validate_slug],
        label="Имя пользователя",
    )
    password = forms.CharField(
        max_length=255,
        validators=[validate_slug],
        label="Пароль",
    )
    email = forms.EmailField(
        label="Электронная почта",
        help_text="Не обязательное",
        required=False,
    )


__all__ = []
