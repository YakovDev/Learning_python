import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card: str | int) -> str:
    """
    Принимает строку с типом и номером карты или счета после преобразует в строку.
    Возвращает строку с замаскированным номером.
    """
    card = str(card)
    if card.count(" ") > 2:
        raise ValueError("Можно вводить только 1 номер счета")
    # Нашел все числа
    match = re.search(r"\d+", card)
    # Проверка на введенный номер если номер счета не передали
    if not match:
        raise ValueError("Номер карты или счета не найден")

    numbers = match.group()
    # Проверяю счет ли это и маскирую номер счета
    if "Счет" in card:
        masked = get_mask_account(numbers)
    else:
        masked = get_mask_card_number(numbers)

    # Возвращаю новую строку с маскировкой счета
    return card.replace(numbers, masked)


def get_date(date: str) -> str:
    r"""
    Функция принимает данные даты в строке iso формата
    извлекает дату месяц год и возвращает
    дату месяц год из строки которую передали
    """
    dt = datetime.fromisoformat(date)
    return dt.strftime("%d.%m.%Y")
