import re
from datetime import datetime

from masks import get_mask_card_number, get_mask_account


def mask_account_card(card: str | None) -> str:
    """
    Принимает строку с типом и номером карты или счета.
    Возвращает строку с замаскированным номером.
    """
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


    Сделал через регулярные выражения потом увидел что надо через datatime...
    Ну ладно попрактиковался хотя-бы оставлю код чтобы посмотрели интересно прочитают или нет)
    #search_year = re.search(r'\d{4}(?=-)', date)
    #search_month = re.search(r"(?<=-)\d{2}(?=-)", date)
    #search_day = re.search(r"(?<=-)\d{2}(?=\w)", date)
    #return f"{str(search_day.group())}.{str(search_month.group())}.{str(search_year.group())}"
    """
    dt = datetime.fromisoformat(date)
    return dt.strftime("%d.%m.%Y")


print(mask_account_card("""Maestro 1596837868705199
Счет 64686473678894779589
MasterCard 7158300734726758"""))
