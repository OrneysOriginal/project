from http import HTTPStatus

from django.test import Client, TestCase


class TestHomepage(TestCase):

    def test_enter(self):
        with self.subTest():
            response = Client().get("/")
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_teapot(self):
        with self.subTest():
            contents = {"Я чайник": 0, "Я кинйач": 0}
            for _ in range(2):
                content = Client().get("/coffee/").content.decode()
                contents[content] += 1
            self.assertEqual(contents["Я чайник"], 1)
            self.assertEqual(contents["Я кинйач"], 1)

    def test_teapot_reverse(self):
        with self.subTest():
            contents = {"Я чайник": 0, "Я кинйач": 0}
            for _ in range(10):
                content = Client().get("/coffee/").content.decode()
                contents[content] += 1
            self.assertEqual(contents["Я чайник"], 9)
            self.assertEqual(contents["Я кинйач"], 1)
