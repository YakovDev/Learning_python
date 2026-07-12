from datetime import datetime
from typing import Any


def filter_by_state(list_of_dict: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция, которая принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует
    указанному значению.

    """
    result = []
    for item in list_of_dict:
        a = item.get("state", "")
        if a == state:
            result.append(item)
    return result


def sort_by_date(list_of_dict: list[dict[str, Any]], procedure: bool = True) -> list[dict[str, Any]]:
    """
    Функция принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """

    return sorted(
        list_of_dict,
        key=lambda x: datetime.fromisoformat(x.get("date", "")) if x.get("date", "") else datetime.min,
        reverse=procedure,
    )
