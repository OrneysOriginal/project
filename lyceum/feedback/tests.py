import pathlib

import django.conf
import django.core.files.base
from django.test import Client, TestCase
from django.urls import reverse
import parameterized

from feedback.forms import FeedbackForm
import feedback.models


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

    @parameterized.parameterized.expand(
        [
            ("I-ne-Taher@yandex.ru", "Привет", 1),
            ("sav1ngeorgiy@yandex.ru", "Привет", 1),
            ("georgijsavin17122@gmail.com", "Привет", 1),
            ("I-ne-Taheryandex.ru", "Привет", 0),
            ("sav1ngeorgiy@yandexru", "Привет", 0),
            ("georgijsavin17122@gmail", "Привет", 0),
        ],
    )
    def test_success_text(self, email, text, is_valid):
        form_data = {
            "text": text,
            "mail": email,
        }
        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        if is_valid:
            try:
                self.assertIn(
                    "Сообщение успешно отправлено",
                    response.content.decode("utf-8"),
                )
            except AssertionError:
                self.assertIn(
                    "еинещбооС оншепсу онелварпто",
                    response.content.decode("utf-8"),
                )
        else:
            with self.assertRaises(AssertionError):
                self.assertIn(
                    "Сообщение успешно отправлено",
                    response.content.decode("utf-8"),
                )

    def test_file_upload(self):
        files = [
            django.core.files.base.ContentFile(
                f"file_{index}".encode(),
                name="filename",
            )
            for index in range(10)
        ]
        form_data = {
            "text": "file_test",
            "mail": "123@mail.com",
            "file": files,
        }
        Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        feedback_files = feedback.models.Feedback.objects.all()

        media_root = pathlib.Path(django.conf.settings.MEDIA_ROOT)

        for index, file in enumerate(feedback_files):
            uploaded_file = media_root / file.file.path
            self.assertEqual(uploaded_file.open().read(), f"file_{index}")


__all__ = []
