import pytest

from src.widget import mask_account_card, get_date


def test_mask_account_account():
    assert mask_account_card("Счет 2345678901012131") == "Счет **2131"


def test_mask_account_card_first():
    assert mask_account_card("Visa 2345678901012131") == "Visa 2345 67** **** 2131"


def test_mask_account_card_second():
    assert mask_account_card(2345678901012131) == "2345 67** **** 2131"


def test_mask_account_card_error_first():
    with pytest.raises(ValueError):
        mask_account_card("Visa")


def test_mask_account_card_error_second():
    with pytest.raises(ValueError):
        mask_account_card("Visa 2345678901012131 Master card 2345678901012131")


def test_get_date():
    assert get_date("2025-03-15T11:30:45.123Z") == "15.03.2025"
    assert get_date("2025-03-15") == "15.03.2025"
