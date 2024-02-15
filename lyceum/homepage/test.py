from django.test import Client, TestCase


class TestHomepage(TestCase):

    def test_enter(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_teapot(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode(), "<body>Я чайник</body>")
