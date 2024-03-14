from http import HTTPStatus
import itertools

import django
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import Client, TestCase
from django.urls import reverse
import parameterized

import catalog.models


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get("/catalog/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("0", HTTPStatus.NOT_FOUND),
            ("1", HTTPStatus.NOT_FOUND),
            ("01", HTTPStatus.NOT_FOUND),
            ("010", HTTPStatus.NOT_FOUND),
            ("10", HTTPStatus.NOT_FOUND),
            ("100", HTTPStatus.NOT_FOUND),
            ("abs", HTTPStatus.NOT_FOUND),
            ("a4s", HTTPStatus.NOT_FOUND),
            ("ab4", HTTPStatus.NOT_FOUND),
            ("4ab", HTTPStatus.NOT_FOUND),
            ("4.323", HTTPStatus.NOT_FOUND),
            ("22^1", HTTPStatus.NOT_FOUND),
            ("$221", HTTPStatus.NOT_FOUND),
            ("221%", HTTPStatus.NOT_FOUND),
            ("-0", HTTPStatus.NOT_FOUND),
            ("-1", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_item_endpoint(
        self,
        param,
        expected_status,
    ):
        try:
            response_status_code = (
                Client()
                .get(reverse("catalog:item_detail", args=[param]))
                .status_code
            )
            template = "catalog:item_detail"
            self.assertEqual(
                response_status_code,
                expected_status,
                msg=f"{reverse(template, args=[param])}"
                f" get not {expected_status}",
            )
        except django.urls.exceptions.NoReverseMatch:
            pass

    @parameterized.parameterized.expand(
        (
            (x[0], x[1][0], x[1][1])
            for x in itertools.product(
                [
                    "re",
                    "converter",
                ],
                [
                    ("1", HTTPStatus.OK),
                    ("10", HTTPStatus.OK),
                    ("100", HTTPStatus.OK),
                    ("01", HTTPStatus.NOT_FOUND),
                    ("010", HTTPStatus.NOT_FOUND),
                    ("0", HTTPStatus.NOT_FOUND),
                    ("-0", HTTPStatus.NOT_FOUND),
                    ("-1", HTTPStatus.NOT_FOUND),
                    ("abs", HTTPStatus.NOT_FOUND),
                    ("a4s", HTTPStatus.NOT_FOUND),
                    ("ab4", HTTPStatus.NOT_FOUND),
                    ("4ab", HTTPStatus.NOT_FOUND),
                    ("4.323", HTTPStatus.NOT_FOUND),
                    ("22^1", HTTPStatus.NOT_FOUND),
                    ("$221", HTTPStatus.NOT_FOUND),
                    ("221%", HTTPStatus.NOT_FOUND),
                ],
            )
        ),
    )
    def test_catalog_item_re_converter_endpoint(
        self,
        prefix,
        param,
        expected_status,
    ):
        respone_status_code = (
            Client().get(f"/catalog/{prefix}/{param}/").status_code
        )
        self.assertEqual(
            respone_status_code,
            expected_status,
            msg=f"/catalog/{prefix}/{param}/ get not {expected_status}",
        )


class DBItemTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Test",
            slug="Test",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Test",
            slug="Test",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "превосходно", True),
            ("test", "роскошно", True),
            ("test", "Я превосходно", True),
            ("test", "превосходно Я", True),
            ("test", "превосходно роскошно", True),
            ("test", "роскошно!", True),
            ("test", "!роскошно", True),
            ("test", "!роскошно", True),
            ("test", "роскошно©", True),
            ("test", "превосходноН", False),
            ("test", "превНосходно", False),
            ("test", "Нпревосходно", False),
            ("test", "Я превосх%одно", False),
            ("test", "превосходнороскошно", False),
            ("test" * 38, "превосходно", False),
        ],
    )
    def test_add_item(self, name, text, is_validate):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=text,
            category=self.category,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)
                self.item.full_clean()
                self.item.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count,
                msg="add no validate item",
            )
        else:
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count + 1,
                msg="no add validate item",
            )


class TagTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", True),
            ("test", "1abs2", True),
            ("test", "a12bs", True),
            ("test", "ABS", True),
            ("test", "-abs-", True),
            ("test", "_abs_", True),
            ("test", "Я", False),
            ("test", "Яabs", False),
            ("test", "Я abs", False),
            ("test", "aЯbs", False),
            ("test", "absЯ", False),
            ("test", "abs Я", False),
            ("test", "*abs*", False),
            ("test", "a*bs", False),
            ("test" * 38, "abs", False),
            ("test", "abs" * 67, False),
        ],
    )
    def test_add_tag(self, name, slug, is_validate):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.tag.full_clean()
                self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count,
                msg="add no validate item",
            )
        else:
            self.tag.full_clean()
            self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 1,
                msg="no add validate item",
            )


class CategoryTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", 1, True),
            ("test", "1abs2", 1, True),
            ("test", "a12bs", 1, True),
            ("test", "ABS", 1, True),
            ("test", "-abs-", 1, True),
            ("test", "_abs_", 1, True),
            ("test", "_abs_", 32767, True),
            ("test", "Я", 1, False),
            ("test", "Яabs", 1, False),
            ("test", "Я abs", 1, False),
            ("test", "aЯbs", 1, False),
            ("test", "absЯ", 1, False),
            ("test", "abs Я", 1, False),
            ("test", "*abs*", 1, False),
            ("test", "a*bs", 1, False),
            ("test" * 38, "abs", 1, False),
            ("test", "abs" * 67, 1, False),
            ("test", "abs", 32768, False),
            ("test", "abs", 0, False),
            ("test", "abs", -1, False),
        ],
    )
    def test_add_category(
        self,
        name,
        slug,
        weight,
        is_validate,
    ):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.category.full_clean()
                self.category.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                category_count,
                msg="add no validate item",
            )
        else:
            self.category.full_clean()
            self.category.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                category_count + 1,
                msg="no add validate item",
            )


class NormalizeNameTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "test test", True),
            ("testfy", "itfaketest", True),
            ("testtrue", "test, test", True),
            ("testyes", "test!test", True),
            ("testtindex", "testt", True),
            ("test!", "test!", False),
            ("!test", "!test", False),
            ("test,", "test,", False),
            (".test", ".test", False),
            ("te st", "te st", False),
            ("te sТ", "te sТ", False),
            ("tеst", "tеst", False),
        ],
    )
    def test_add_tag(self, name1, name2, is_validate):
        tag_count = catalog.models.Category.objects.count()
        self.tag1 = catalog.models.Tag(
            name=name1,
            slug="1",
        )
        self.tag2 = catalog.models.Tag(
            name=name2,
            slug="2",
        )
        if not is_validate:
            with self.assertRaises(
                ValidationError,
                msg=f"add {name2} but we have {name1}",
            ):
                self.tag1.full_clean()
                self.tag1.save()
                self.tag2.full_clean()
                self.tag2.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 1,
                msg="add no validate item",
            )
        else:
            self.tag1.full_clean()
            self.tag1.save()
            self.tag2.full_clean()
            self.tag2.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 2,
                msg="no add validate item",
            )


class PagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Test",
            slug="Test",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Test",
            slug="Test",
        )
        cls.tag.save()
        cls.category.save()

    @parameterized.parameterized.expand(
        [
            (reverse("catalog:item_list"), HTTPStatus.OK),
            (reverse("catalog:item_detail", args=[0]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[1]), HTTPStatus.OK),
            (reverse("catalog:item_detail", args=[2]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[3]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[4]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[5]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[6]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[7]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[8]), HTTPStatus.NOT_FOUND),
            (reverse("catalog:item_detail", args=[9]), HTTPStatus.NOT_FOUND),
        ],
    )
    def test_page_status_code(self, url, status_code):
        item = catalog.models.Item.objects.create(
            name="Test",
            text="Test",
            category=self.category,
        )
        item.clean()
        item.save()
        response_code = Client().get(url).status_code
        self.assertEqual(response_code, status_code)


class ContextTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.publish_category = catalog.models.Category.objects.create(
            name="Тестовая категория опубликован",
            is_published=True,
            slug="Test slug",
            weight=200,
        )

    def test_homepage(self):
        item = catalog.models.Item.objects.create(
            name="Test",
            is_published=True,
            category=self.publish_category,
        )
        item.clean()
        item.save()
        response = django.test.Client().get(reverse("homepage:main"))
        self.assertIn("items", response.context)

    @parameterized.parameterized.expand(
        [
            ("test_name", True, "test_text превосходно", 1),
            ("test_name", False, "test_text превосходно", 0),
        ],
    )
    def test_homepage_count_item(
        self,
        name,
        is_published,
        text,
        count,
    ):
        item = catalog.models.Item.objects.create(
            name=name,
            is_published=is_published,
            category=self.publish_category,
            text=text,
        )
        item.full_clean()
        item.save()
        response = django.test.Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(len(items), count)

    @parameterized.parameterized.expand(
        [
            ("homepage:main", QuerySet),
            ("catalog:item_list", QuerySet),
            ("about:about", QuerySet),
        ],
    )
    def test_type_context(self, url, datastruct):
        response = django.test.Client().get(reverse(url))
        self.assertIsInstance(response.context["items"], datastruct)


__all__ = []
