from django.test import Client, TestCase
from django.urls import reverse
import parameterized

from feedback.forms import FeedbackForm


class TestFeedback(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    @parameterized.parameterized.expand(
        [
            ("I-ne-Taher@yandex.ru", "Привет"),
            ("sav1ngeorgiy@yandex.ru", "Привет"),
            ("georgijsavin17122@gmail.com", "Привет"),
        ],
    )
    def test_redirect_feedback(self, email, text):
        form_data = {
            "text": text,
            "mail": email,
        }
        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_label(self):
        text_label_name = TestFeedback.form.fields["text"].label
        mail_label_name = TestFeedback.form.fields["mail"].label
        self.assertEqual(text_label_name, "Текст для письма")
        self.assertEqual(mail_label_name, "Электронная почта")

    def test_help_text(self):
        text_for_help = TestFeedback.form.fields["text"].help_text
        mail_for_help = TestFeedback.form.fields["mail"].help_text
        self.assertEqual(text_for_help, "Введите текст для письма")
        self.assertEqual(mail_for_help, "Введите вашу почту")

    def test_context(self):
        form_data = {
            "text": "Привет",
            "mail": "georgijsavin17122@gmail.com",
        }
        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertIn("form", response.context)


__all__ = []
