from http import HTTPStatus
import itertools

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
import parameterized

import catalog.models


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self) -> None:
        status_code = Client().get("/catalog/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("0", HTTPStatus.OK),
            ("1", HTTPStatus.OK),
            ("01", HTTPStatus.OK),
            ("010", HTTPStatus.OK),
            ("10", HTTPStatus.OK),
            ("100", HTTPStatus.OK),
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
        param: str,
        expected_status: HTTPStatus,
    ) -> None:
        respone_status_code = Client().get(f"/catalog/{param}/").status_code
        self.assertEqual(
            respone_status_code,
            expected_status,
            msg=f"/catalog/{param}/ get not {expected_status}",
        )

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
        prefix: str,
        param: str,
        expected_status: HTTPStatus,
    ) -> None:
        respone_status_code = (
            Client().get(f"/catalog/{prefix}/{param}/").status_code
        )
        self.assertEqual(
            respone_status_code,
            expected_status,
            msg=f"/catalog/{prefix}/{param}/ get not {expected_status}",
        )


class DBItemTests(TestCase):
    category: catalog.models.Category
    tag: catalog.models.Tag

    @classmethod
    def setUpClass(cls) -> None:
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
    def test_add_item(self, name: str, text: str, is_validate: bool) -> None:
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
    def test_add_tag(self, name: str, slug: str, is_validate: bool) -> None:
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
                catalog.models.Item.objects.count(),
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
        name: str,
        slug: str,
        weight: int,
        is_validate: bool,
    ) -> None:
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
        (
            (x[0], x[1][0], x[1][1])
            for x in itertools.product(
                [
                    ("test"),
                    ("Тest"),
                    ("tЕst"),
                ],
                [
                    ("test test", True),
                    ("itfaketest", True),
                    ("test, test", True),
                    ("test!test", True),
                    ("testt", True),
                    ("test!", False),
                    ("!test", False),
                    ("!test!", False),
                    (" test ", False),
                    ("test,", False),
                    (".test", False),
                    ("te st", False),
                    ("te sТ", False),
                    ("tеst", False),
                ],
            )
        ),
    )
    def test_add_tag(self, name1: str, name2: str, is_validate: bool) -> None:
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
