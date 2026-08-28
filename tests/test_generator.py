from typing import Any

import pytest

from src.generator import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(transactions: list[dict[str, Any]]) -> None:
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 3


def test_filter_by_currency_value_errors(transactions: list[dict[str, Any]]) -> None:
    result = filter_by_currency(transactions, "CNY")
    result_2 = filter_by_currency([], "CNY")
    assert list(result) == []
    assert list(result_2) == []


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, "Перевод в кафе"),
        (1, "Покупка в магазине"),
        (2, "Оплата подписки"),
        (3, ""),
        (4, None),  # для транзакции без описания
        (5, "Без валюты"),
        (6, "Перевод другу"),
    ],
)
def test_transaction_descriptions(transactions: list[dict[str, Any]], index: int, expected: Any) -> None:
    gen = transaction_descriptions(transactions)
    for _ in range(index):
        next(gen)
    assert next(gen) == expected


def test_transaction_descriptions_usd_iter_check(transactions: list[dict[str, Any]]) -> None:
    result_3 = transaction_descriptions([])
    assert list(result_3) == []


def test_card_number_generator() -> None:
    with pytest.raises(ValueError):
        list(card_number_generator(1111111111111111111, 222222222222222222222))


def test_card_number_generator_iter_check() -> None:
    assert list(card_number_generator(1, 3)) == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]


def test_card_number_generator_check_start() -> None:
    assert list(card_number_generator(3, 1)) == []
