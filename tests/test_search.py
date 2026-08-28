import pytest
from typing import Any

from src.search import process_bank_search, count_operations_by_category


@pytest.mark.parametrize(
    ["search_word", "expected_ids"],
    [
        ("кафе", [1]),
        ("магазин", [2]),
        ("подписки", [3]),
        ("другу", [7]),
        ("перевод", [1, 7]),  # слово встречается в нескольких
        ("несуществующее", []),
        ("", [1, 2, 3, 4, 5, 6, 7]),  # пустой поиск – возвращается все
    ],
)
def test_process_bank_search(transactions: list[dict[str, Any]], search_word: str, expected_ids: list[int]) -> None:
    result = process_bank_search(transactions, search_word)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


@pytest.mark.parametrize(
    ["categories", "expected_ids"],
    [
        ("кафе", {"а": 1, "е": 1, "к": 3, "ф": 0}),
        ("магазин", {"а": 3, "г": 1, "з": 0, "и": 0, "м": 1, "н": 0}),
        ("подписки", {"д": 0, "и": 0, "к": 0, "о": 0, "п": 4, "с": 0}),
        ("другу", {"г": 0, "д": 3, "р": 0, "у": 1}),
        ("перевод", {"в": 0, "д": 0, "е": 1, "о": 0, "п": 4, "р": 0}),
        ("несуществующее", {"в": 0, "е": 3, "н": 1, "с": 1, "т": 0, "у": 0, "щ": 0, "ю": 0}),
        ("", {}),  # пустой поиск – возвращается пустой словарь
    ],
)
def test_count_operations_by_category(
    transactions: list[dict[str, Any]], categories: list[str], expected_ids: list[int]
) -> None:
    result = count_operations_by_category(transactions, categories)
    assert result == expected_ids
