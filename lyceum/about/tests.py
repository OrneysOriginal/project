from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
import parameterized


class TestAbout(TestCase):

    def test_about(self):
        response = Client().get("/about/")
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PageTests(TestCase):
    @parameterized.parameterized.expand(
        [
            (reverse("about:about"), 200),
        ],
    )
    def test_page_status_code(self, url, status_code):
        response = Client().get(url).status_code
        self.assertEqual(response, status_code)


__all__ = []
