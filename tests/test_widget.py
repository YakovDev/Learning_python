import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_account() -> None:
    assert mask_account_card("Счет 2345678901012131") == "Счет **2131"


def test_mask_account_card_first() -> None:
    assert mask_account_card("Visa 2345678901012131") == "Visa 2345 67** **** 2131"


def test_mask_account_card_second() -> None:
    assert mask_account_card(2345678901012131) == "2345 67** **** 2131"


def test_mask_account_card_error_first() -> None:
    assert mask_account_card("Visa") == "Visa"


def test_mask_account_card_error_second() -> None:
    assert (
        mask_account_card("Visa 2345678901012131 Master card 2345678901012131")
        == "Visa 2345 67** **** 2131 Master card 2345 67** **** 2131"
    )


def test_get_date() -> None:
    assert get_date("2025-03-15T11:30:45.123Z") == "15.03.2025"
    assert get_date("2025-03-15") == "15.03.2025"


def test_get_date_exception() -> None:
    assert get_date("2") == "Дата неизвестна"
