import re
from datetime import datetime

from masks import get_mask_card_number, get_mask_account


def mask_account_card(card: str) -> str:
    """
    Принимает строку с типом и номером карты или счета.
    Возвращает строку с замаскированным номером.
    """
    # Нашел все числа
    match = re.search(r"\d+", card)
    # Проверка на введенный номер если
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
    """
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


print(get_date("2024-03-11T02:26:18.671407"))
