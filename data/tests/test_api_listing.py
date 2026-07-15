"""Contract tests for list pagination, search, filtering, and ordering."""

from types import SimpleNamespace

from django.http import QueryDict
from django.test import SimpleTestCase

from data.api.listing import MAX_PAGE_SIZE, paginate_list
from data.utils.exceptions import InvalidParameter


class FakeRequest(SimpleNamespace):
    def build_absolute_uri(self, value):
        return f"https://api.example.test{value}"


def request_for(query=""):
    return FakeRequest(query_params=QueryDict(query), path="/api/v1/data/items/")


class ListQueryContractTests(SimpleTestCase):
    def setUp(self):
        self.items = [
            {"code": "3", "name": "Gamma", "city": "Limpio"},
            {"code": "1", "name": "Alpha", "city": "Asuncion"},
            {"code": "2", "name": "Beta", "city": "Limpio"},
        ]

    def test_returns_stable_page_envelope_and_navigation_links(self):
        response = paginate_list(
            request_for("page=1&page_size=2"),
            self.items,
            ordering_fields=("name",),
            default_ordering="name",
        )

        self.assertEqual(response["count"], 3)
        self.assertIsNone(response["previous"])
        self.assertIn("page=2", response["next"])
        self.assertEqual([item["name"] for item in response["results"]], ["Alpha", "Beta"])

    def test_returns_previous_link_on_later_page(self):
        response = paginate_list(request_for("page=2&page_size=2"), self.items)

        self.assertIn("page=1", response["previous"])
        self.assertIsNone(response["next"])
        self.assertEqual(len(response["results"]), 1)

    def test_search_is_case_insensitive_and_allowlisted(self):
        response = paginate_list(
            request_for("search=alp"),
            self.items,
            search_fields=("name",),
        )

        self.assertEqual(response["count"], 1)
        self.assertEqual(response["results"][0]["name"], "Alpha")

    def test_filtering_uses_only_declared_fields(self):
        response = paginate_list(
            request_for("city=Limpio&code=1"),
            self.items,
            filter_fields=("city",),
        )

        self.assertEqual(response["count"], 2)
        self.assertTrue(all(item["city"] == "Limpio" for item in response["results"]))

    def test_ordering_supports_ascending_and_descending(self):
        ascending = paginate_list(
            request_for("ordering=name"), self.items, ordering_fields=("name",)
        )
        descending = paginate_list(
            request_for("ordering=-name"), self.items, ordering_fields=("name",)
        )

        self.assertEqual(ascending["results"][0]["name"], "Alpha")
        self.assertEqual(descending["results"][0]["name"], "Gamma")

    def test_page_size_is_capped(self):
        items = [{"code": str(index)} for index in range(MAX_PAGE_SIZE + 5)]
        response = paginate_list(request_for("page_size=999"), items)

        self.assertEqual(len(response["results"]), MAX_PAGE_SIZE)
        self.assertIsNotNone(response["next"])

    def test_invalid_page_and_ordering_are_rejected(self):
        with self.assertRaises(InvalidParameter):
            paginate_list(request_for("page=zero"), self.items)
        with self.assertRaises(InvalidParameter):
            paginate_list(
                request_for("ordering=private_field"),
                self.items,
                ordering_fields=("name",),
            )
