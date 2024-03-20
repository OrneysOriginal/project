from django.forms import ModelForm

from homepage.models import EchoSubmit


class BootstrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input-group-text"


class EchoSubmitForm(BootstrapForm):
    class Meta:
        model = EchoSubmit
        fields = (EchoSubmit.text.field.name,)
        labels = {
            EchoSubmit.text.field.name: "Текст",
        }


__all__ = []
