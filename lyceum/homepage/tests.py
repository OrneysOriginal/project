from http import HTTPStatus

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


__all__ = []
