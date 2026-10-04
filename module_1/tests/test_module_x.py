"""Unit tests for module_x.py public functions."""

import pytest

from module_x import (
    calculate_discount,
    classify_priority,
    is_valid_project_code,
    normalize_name,
    summarize_order,
)


class TestNormalizeName:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("jane doe", "Jane Doe"),
            ("  jane   doe  ", "Jane Doe"),
            ("JANE DOE", "Jane Doe"),
            ("jane", "Jane"),
            ("mary-jane o'brien", "Mary-Jane O'Brien"),
        ],
    )
    def test_cleans_and_title_cases(self, raw, expected):
        assert normalize_name(raw) == expected

    def test_raises_type_error_for_non_string(self):
        with pytest.raises(TypeError):
            normalize_name(123)

    @pytest.mark.parametrize("raw", ["", "   ", "\t\n"])
    def test_raises_value_error_for_empty(self, raw):
        with pytest.raises(ValueError):
            normalize_name(raw)


class TestCalculateDiscount:
    @pytest.mark.parametrize(
        "price, tier, expected",
        [
            (100.0, "standard", 100.0),
            (100.0, "silver", 95.0),
            (100.0, "gold", 90.0),
            (100.0, "platinum", 85.0),
            (100.0, "GOLD", 90.0),
            (100.0, "  silver  ", 95.0),
            (0.0, "platinum", 0.0),
        ],
    )
    def test_applies_tier_rate(self, price, tier, expected):
        assert calculate_discount(price, tier) == expected

    def test_rounds_to_two_decimals(self):
        assert calculate_discount(10.005, "silver") == round(10.005 * 0.95, 2)

    def test_raises_value_error_for_negative_price(self):
        with pytest.raises(ValueError):
            calculate_discount(-1.0, "gold")

    def test_raises_value_error_for_unknown_tier(self):
        with pytest.raises(ValueError):
            calculate_discount(100.0, "diamond")


class TestClassifyPriority:
    @pytest.mark.parametrize(
        "score, expected",
        [
            (0, "low"),
            (39, "low"),
            (40, "medium"),
            (69, "medium"),
            (70, "high"),
            (89, "high"),
            (90, "urgent"),
            (100, "urgent"),
        ],
    )
    def test_classifies_boundaries(self, score, expected):
        assert classify_priority(score) == expected

    def test_raises_type_error_for_non_int(self):
        with pytest.raises(TypeError):
            classify_priority(50.0)

    @pytest.mark.parametrize("score", [-1, 101])
    def test_raises_value_error_out_of_range(self, score):
        with pytest.raises(ValueError):
            classify_priority(score)


class TestSummarizeOrder:
    def test_empty_order(self):
        assert summarize_order([]) == {"item_count": 0, "subtotal": 0.0}

    def test_single_item(self):
        items = [{"quantity": 2, "unit_price": 3.5}]
        assert summarize_order(items) == {"item_count": 2, "subtotal": 7.0}

    def test_multiple_items(self):
        items = [
            {"quantity": 1, "unit_price": 10.0},
            {"quantity": 3, "unit_price": 2.25},
        ]
        assert summarize_order(items) == {"item_count": 4, "subtotal": 16.75}

    def test_missing_fields_default_to_zero(self):
        assert summarize_order([{}]) == {"item_count": 0, "subtotal": 0.0}

    def test_rounds_subtotal(self):
        items = [{"quantity": 3, "unit_price": 0.1}]
        result = summarize_order(items)
        assert result["subtotal"] == round(0.3, 2)

    def test_raises_value_error_for_negative_quantity(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": -1, "unit_price": 1.0}])

    def test_raises_value_error_for_non_int_quantity(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": 1.5, "unit_price": 1.0}])

    def test_raises_value_error_for_negative_unit_price(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": 1, "unit_price": -1.0}])

    def test_raises_value_error_for_non_numeric_unit_price(self):
        with pytest.raises(ValueError):
            summarize_order([{"quantity": 1, "unit_price": "free"}])


class TestIsValidProjectCode:
    @pytest.mark.parametrize(
        "code",
        ["AB-1234", "ZZ-0000", "QX-9999"],
    )
    def test_valid_codes(self, code):
        assert is_valid_project_code(code) is True

    @pytest.mark.parametrize(
        "code",
        [
            "ab-1234",  # lowercase prefix
            "ABC-1234",  # prefix too long
            "A-1234",  # prefix too short
            "AB-123",  # number too short
            "AB-12345",  # number too long
            "AB1234",  # missing separator
            "AB-12A4",  # non-digit in number
            "1B-1234",  # non-alpha prefix
            "",
            "AB-1234-5",
        ],
    )
    def test_invalid_codes(self, code):
        assert is_valid_project_code(code) is False

    def test_non_string_input_returns_false(self):
        assert is_valid_project_code(1234) is False
