from http import HTTPStatus

from django.db.models import QuerySet
import django.test
from django.test import Client, TestCase
from django.urls import reverse
import parameterized


class TestHomepage(TestCase):

    def test_enter(self):
        with self.subTest():
            response = Client().get("/")
            self.assertEqual(response.status_code, HTTPStatus.OK)


class PagesTests(TestCase):
    @parameterized.parameterized.expand(
        [
            (reverse("homepage:main"), 200),
        ],
    )
    def test_page_status_code(self, url, status_code):
        response = Client().get(url).status_code
        self.assertEqual(response, status_code)

    @parameterized.parameterized.expand(
        [
            ("homepage:main", "items"),
        ],
    )
    def test_homepage(self, url, key):
        response = django.test.Client().get(reverse(url))
        self.assertIn(key, response.context)

    @parameterized.parameterized.expand(
        [
            ("homepage:main", QuerySet),
        ],
    )
    def test_type_context(self, url, datastruct):
        response = django.test.Client().get(reverse(url))
        self.assertIsInstance(response.context["items"], datastruct)


class FormTests(TestCase):

    @parameterized.parameterized.expand(
        [
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет"),
            ("Привет, этo почтi-почти Pуcский текст@, "
             "просто≈ Как-то со спецü символами:) ¡сорри∑! "
             "Hу ещё раз ¡сорри! Ёжика не видели?"),
        ]
    )
    def test_form(self, text):
        response = Client().post(
            "echo/submit/",
            text=text,
        )
        self.assertRedirects(response, "echo/submit/")



__all__ = []
