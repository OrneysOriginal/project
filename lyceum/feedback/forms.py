from django.forms import EmailInput, ModelForm, TextInput

from feedback.models import Feedback


class FeedbackForm(ModelForm):
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
        widgets = {
            "text": TextInput(attrs={"class": "input-group-text"}),
            "mail": EmailInput(attrs={"class": "input-group-text"}),
        }


__all__ = []
