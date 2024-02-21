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

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test_category-slug",
            weight=100,
        )

    def test_add_not_valid_item(self):
        item_count = catalog.models.Item.objects.count()
        item_bases_not_valid = [
            catalog.models.Item(
                name="Тестовый товар",
                category=self.category,
                text="Не валидный текст",
                is_published=True,
            )
            for _ in range(5)
        ]
        with self.assertRaises(django.core.exceptions.ValidationError):
            for i in range(5):
                item_bases_not_valid[i].name += str(i)
            item_bases_not_valid[0].text = "Превосходный"
            item_bases_not_valid[1].text = "Роскошно123"
            item_bases_not_valid[2].text = "роскошно123"
            item_bases_not_valid[3].text = "и превосходное и роскошное"
            item_bases_not_valid[4].text = "1Роскошно"
            for i in range(len(item_bases_not_valid)):
                item_bases_not_valid[i].full_clean()
                item_bases_not_valid[i].save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    def test_add_valid_item(self):
        item_count = catalog.models.Item.objects.count()
        item_bases_valid = [
            catalog.models.Item(
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
            catalog.models.Item.objects.count(),
            item_count + 5,
        )

    def test_add_not_valid_category(self):
        category_count = catalog.models.Category.objects.count()
        category_bases_not_valid = [
            catalog.models.Category(
                name="Тестовое имя",
                is_published=True,
                slug="testing_slug",
                weight=100,
            )
            for _ in range(5)
        ]
        with self.assertRaises(django.core.exceptions.ValidationError):
            for i in range(len(category_bases_not_valid)):
                category_bases_not_valid[i].name += str(i)
                category_bases_not_valid[i].slug += str(i)
                category_bases_not_valid[i].weight -= 100
                category_bases_not_valid[i].full_clean()
                category_bases_not_valid[i].save()
        category_bases_not_valid = [
            catalog.models.Category(
                name="Тестовое имя",
                is_published=True,
                slug="testing_slug",
                weight=100,
            )
            for _ in range(5)
        ]
        with self.assertRaises(django.core.exceptions.ValidationError):
            for i in range(len(category_bases_not_valid)):
                category_bases_not_valid[i].name += str(i)
                category_bases_not_valid[i].slug += str(i)
                category_bases_not_valid[i].weight += 300000
                category_bases_not_valid[i].full_clean()
                category_bases_not_valid[i].save()
        self.assertEqual(
            catalog.models.Category.objects.count(), category_count,
        )

    def test_add_valid_category(self):
        category_count = catalog.models.Category.objects.count()
        category_bases_not_valid = [
            catalog.models.Category(
                name="Тестовое имя",
                is_published=True,
                slug="testing_slug",
                weight=100,
            )
            for _ in range(5)
        ]
        for i in range(len(category_bases_not_valid)):
            category_bases_not_valid[i].name += str(i)
            category_bases_not_valid[i].slug += str(i)
            category_bases_not_valid[i].weight += i
            category_bases_not_valid[i].full_clean()
            category_bases_not_valid[i].save()
        self.assertEqual(
            catalog.models.Category.objects.count(), category_count + 5,
        )

    def test_add_not_valid_tag(self):
        tag_count = catalog.models.Tag.objects.count()
        items_bases_not_valid = [
            catalog.models.Tag(
                name="Тестовое имя",
                is_published=True,
                slug="testing_not_valid_slug",
            )
            for _ in range(5)
        ]
        with self.assertRaises(django.core.exceptions.ValidationError):
            for i in range(5):
                items_bases_not_valid[i].name += str(i)
            items_bases_not_valid[0].slug = "тест"
            items_bases_not_valid[1].slug = "123т"
            items_bases_not_valid[2].slug = "Ааaaa"
            items_bases_not_valid[3].slug = "Uф"
            items_bases_not_valid[4].slug = "qйq"
            for i in range(5):
                items_bases_not_valid[i].full_clean()
                items_bases_not_valid[i].save()
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count)

    def test_add_valid_tag(self):
        tag_count = catalog.models.Tag.objects.count()
        items_bases_valid = [
            catalog.models.Tag(
                name="Тестовое имя",
                is_published=True,
                slug="testing_valid_slug",
            )
            for _ in range(5)
        ]
        items_bases_valid[0].slug = "qwerty1"
        items_bases_valid[1].slug = "qwerty2"
        items_bases_valid[2].slug = "Abacaba_3"
        items_bases_valid[3].slug = "_123_4"
        items_bases_valid[4].slug = "qwer_123_ty5"
        for i in range(5):
            items_bases_valid[i].name += str(i)
        for i in range(5):
            items_bases_valid[i].full_clean()
            items_bases_valid[i].save()
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 5)
