from django.forms import ModelForm, TextInput

from homepage.models import EchoSubmit


class EchoSubmitForm(ModelForm):
    class Meta:
        model = EchoSubmit
        fields = "__all__"
        labels = {
            EchoSubmit.text.field.name: "Текст",
        }
        widgets = {
            "text": TextInput(attrs={"class": "input-group-text"}),
        }


__all__ = []
