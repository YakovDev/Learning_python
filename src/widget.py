import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card: str | int) -> str:
    """
    Принимает строку с типом и номером карты или счета после преобразует в строку.
    Возвращает строку с замаскированным номером.
    """
    card = str(card)
    match = re.search(r"\d+", card)
    if not match:
        return card

    numbers = match.group()
    if "Счет" in card:
        masked = get_mask_account(numbers)
    else:
        masked = get_mask_card_number(numbers)

    return card.replace(numbers, masked)


def get_date(date: str) -> str:
    r"""
    Функция принимает данные даты в строке iso формата
    извлекает дату месяц год и возвращает
    дату месяц год из строки которую передали
    """
    try:
        dt = datetime.fromisoformat(date)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return "Дата неизвестна"
