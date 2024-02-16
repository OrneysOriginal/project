from http import HTTPStatus

from django.test import Client, TestCase


class TestHomepage(TestCase):

    def test_enter(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_teapot(self):
        lst = []
        for i in range(9):
            lst.append(Client().get("/coffee/"))
        for i in range(len(lst)):
            self.assertEqual(lst[i].status_code, HTTPStatus.IM_A_TEAPOT)
            if i == 0:
                self.assertEqual(lst[i].content.decode(), "Я кинйач")
            else:
                self.assertEqual(lst[i].content.decode(), "Я чайник")
