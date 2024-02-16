from http import HTTPStatus

from django.test import Client, TestCase


class TestHomepage(TestCase):

    def test_enter(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_teapot(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")

    def test_teapot_reverse(self):
        responses = []
        for i in range(10):
            responses.append(Client().get("/coffee/").content.decode())
        self.assertEqual(responses.count("Я кинйач"), 1)


