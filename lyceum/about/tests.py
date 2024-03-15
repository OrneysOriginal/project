from http import HTTPStatus

import django
from django.db.models import QuerySet
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

    @parameterized.parameterized.expand(
        [
            ("about:about", QuerySet),
        ],
    )
    def test_type_context(self, url, datastruct):
        response = django.test.Client().get(reverse(url))
        self.assertIs(response.context["items"], datastruct)

    @parameterized.parameterized.expand(
        [
            ("about:about", "items"),
        ],
    )
    def test_about(self, url, key):
        response = django.test.Client().get(reverse(url))
        self.assertIn(key, response.context)


__all__ = []
