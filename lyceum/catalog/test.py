from django.test import Client, TestCase


class TestCatalog(TestCase):

    def test_catalog(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_conv(self):
        response = Client().get("/catalog/1")
        self.assertEqual(response.status_code, 200)
