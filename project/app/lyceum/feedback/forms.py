from django.forms import ModelForm

from feedback.models import Feedback


class BootstrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input-group-text"


class FeedbackForm(BootstrapForm):
    class Meta:
        model = Feedback
        exclude = ["created_on"]

        labels = {
            Feedback.text.field.name: "Текст для письма",
            Feedback.mail.field.name: "Электронная почта",
        }
        help_texts = {
            Feedback.mail.field.name: "Введите вашу почту",
            Feedback.text.field.name: "Введите текст для письма",
        }


__all__ = []
