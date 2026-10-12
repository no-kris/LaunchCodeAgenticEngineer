"""Unit tests for module_1/module_x.py."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from module_x import (  # noqa: E402
    VALID_CUSTOMER_TIERS,
    calculate_discount,
    classify_priority,
    is_valid_project_code,
    normalize_name,
    summarize_order,
)


class TestNormalizeName(unittest.TestCase):
    def test_title_cases_words(self):
        self.assertEqual(normalize_name("ada lovelace"), "Ada Lovelace")

    def test_collapses_and_strips_whitespace(self):
        self.assertEqual(normalize_name("  grace \t\n  HOPPER  "), "Grace Hopper")

    def test_single_word(self):
        self.assertEqual(normalize_name("alan"), "Alan")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            normalize_name("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            normalize_name("   \t\n ")

    def test_non_string_raises_type_error(self):
        for bad in (None, 123, ["ada"]):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                normalize_name(bad)


class TestCalculateDiscount(unittest.TestCase):
    def test_each_tier_rate(self):
        expected = {
            "standard": 100.0,
            "silver": 95.0,
            "gold": 90.0,
            "platinum": 85.0,
        }
        self.assertEqual(set(expected), VALID_CUSTOMER_TIERS)
        for tier, price in expected.items():
            with self.subTest(tier=tier):
                self.assertEqual(calculate_discount(100, tier), price)

    def test_tier_is_case_and_whitespace_insensitive(self):
        self.assertEqual(calculate_discount(100, "  GoLd "), 90.0)

    def test_rounds_to_two_decimals(self):
        self.assertEqual(calculate_discount(19.99, "silver"), 18.99)

    def test_zero_price(self):
        self.assertEqual(calculate_discount(0, "platinum"), 0.0)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            calculate_discount(-0.01, "gold")

    def test_unknown_tier_raises(self):
        with self.assertRaisesRegex(ValueError, "unknown customer tier: bronze"):
            calculate_discount(10, "bronze")


class TestClassifyPriority(unittest.TestCase):
    def test_boundaries(self):
        cases = {
            0: "low",
            39: "low",
            40: "medium",
            69: "medium",
            70: "high",
            89: "high",
            90: "urgent",
            100: "urgent",
        }
        for score, expected in cases.items():
            with self.subTest(score=score):
                self.assertEqual(classify_priority(score), expected)

    def test_out_of_range_raises(self):
        for score in (-1, 101):
            with self.subTest(score=score), self.assertRaises(ValueError):
                classify_priority(score)

    def test_non_int_raises_type_error(self):
        for bad in (50.0, "50", None):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                classify_priority(bad)


class TestSummarizeOrder(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(summarize_order([]), {"item_count": 0, "subtotal": 0.0})

    def test_none_treated_as_empty(self):
        self.assertEqual(summarize_order(None), {"item_count": 0, "subtotal": 0.0})

    def test_multiple_items(self):
        items = [
            {"name": "widget", "quantity": 2, "unit_price": 3.50},
            {"name": "gadget", "quantity": 1, "unit_price": 10},
        ]
        self.assertEqual(summarize_order(items), {"item_count": 3, "subtotal": 17.0})

    def test_subtotal_rounded(self):
        items = [{"quantity": 3, "unit_price": 0.1}]
        self.assertEqual(summarize_order(items)["subtotal"], 0.3)

    def test_missing_keys_default_to_zero(self):
        self.assertEqual(summarize_order([{}]), {"item_count": 0, "subtotal": 0.0})

    def test_invalid_quantity_raises(self):
        for bad in (-1, 1.5, "2"):
            with self.subTest(quantity=bad), self.assertRaises(ValueError):
                summarize_order([{"quantity": bad, "unit_price": 1.0}])

    def test_invalid_unit_price_raises(self):
        for bad in (-0.01, "1.00", None):
            with self.subTest(unit_price=bad), self.assertRaises(ValueError):
                summarize_order([{"quantity": 1, "unit_price": bad}])


class TestIsValidProjectCode(unittest.TestCase):
    def test_valid_codes(self):
        for code in ("AB-1234", "ZZ-0000"):
            with self.subTest(code=code):
                self.assertTrue(is_valid_project_code(code))

    def test_invalid_codes(self):
        for code in (
            "",
            "AB1234",
            "ab-1234",
            "Ab-1234",
            "ABC-1234",
            "A-1234",
            "AB-123",
            "AB-12345",
            "AB-12a4",
            "A1-1234",
            "AB-12-34",
            " AB-1234",
        ):
            with self.subTest(code=code):
                self.assertFalse(is_valid_project_code(code))

    def test_non_string_returns_false(self):
        for bad in (None, 1234, ["AB-1234"]):
            with self.subTest(bad=bad):
                self.assertFalse(is_valid_project_code(bad))


if __name__ == "__main__":
    unittest.main()
