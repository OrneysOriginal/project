from django.test import Client, TestCase


class TestCatalog(TestCase):

    def test_catalog(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_conv(self):
        response = Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)

    def test_some_re(self):
        response = Client().get("/catalog/re/1/")
        self.assertEqual(response.status_code, 200)
        response = Client().get("/catalog/re/1/0")
        self.assertEqual(response.status_code, 404)
        response = Client().get("/catalog/re/99/")
        self.assertEqual(response.status_code, 200)
        response = Client().get("/catalog/re/'99'/")
        self.assertEqual(response.status_code, 404)
