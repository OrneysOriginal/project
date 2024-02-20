from http import HTTPStatus

import catalog.models
import django.core.exceptions
from django.test import Client, TestCase


class TestCatalog(TestCase):

    def test_catalog(self):
        with self.subTest():
            response = Client().get("/catalog/")
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_conv(self):
        with self.subTest():
            response = Client().get("/catalog/1/")
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_some_re(self):
        with self.subTest():
            response = Client().get("/catalog/re/1/")
            self.assertEqual(response.status_code, HTTPStatus.OK)
            response = Client().get("/catalog/re/1/0")
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            response = Client().get("/catalog/re/99/")
            self.assertEqual(response.status_code, HTTPStatus.OK)
            response = Client().get("/catalog/re/'99'/")
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            response = Client().get("/catalog/re/0/")
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.CatalogCategory.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test_category-slug",
            weight=100,
        )

    def test_add_not_valid_item(self):
        item_count = catalog.models.CatalogItem.objects.count()
        item_base = catalog.models.CatalogItem(
            name="Тестовый товар",
            category=self.category,
            text="Не валидный текст",
            is_published=True,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            item_bases_not_valid = [item_base for _ in range(5)]
            item_bases_not_valid[0].text = "Превосходный"
            item_bases_not_valid[1].text = "Роскошно123"
            item_bases_not_valid[2].text = "роскошно123"
            item_bases_not_valid[3].text = "и превосходное и роскошное"
            item_bases_not_valid[4].text = "1Роскошно"
            for i in range(len(item_bases_not_valid)):
                item_bases_not_valid[i].full_clean()
                item_bases_not_valid[i].save()

        self.assertEqual(
            catalog.models.CatalogItem.objects.count(),
            item_count,
        )

    def test_add_valid_item(self):
        item_count = catalog.models.CatalogItem.objects.count()
        item_bases_valid = [
            catalog.models.CatalogItem(
                name="Тестовый товар",
                category=self.category,
                text="Валидный текст",
                is_published=True,
            )
            for _ in range(5)
        ]
        item_bases_valid[0].text = "Отлично,превосходно"
        item_bases_valid[1].text = "Превосходно"
        item_bases_valid[2].text = "роскошно"
        item_bases_valid[3].text = "РоСкОшНо"
        item_bases_valid[4].text = "Превосходно и Роскошно"
        for i in range(len(item_bases_valid)):
            item_bases_valid[i].full_clean()
            item_bases_valid[i].save()

        self.assertEqual(
            catalog.models.CatalogItem.objects.count(),
            item_count + 5,
        )
