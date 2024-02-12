from django.test import Client, TestCase


class TestHomepage(TestCase):

    def test_enter(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)
