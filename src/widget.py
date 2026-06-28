import re

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


print(mask_account_card("Visa Platinum 7000792289606362"))
