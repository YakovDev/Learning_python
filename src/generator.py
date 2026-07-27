def filter_by_currency(transactions: list[dict], currency: str):
    """

    Функция принимает на вход список словарей, представляющих транзакции.
    Функция должна возвращать итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)

    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("name") == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]):
    """ """
    for transaction in transactions:
        if transaction.get("description", {}):
            yield transaction.get("description", {})


def card_number_generator(start: int, end: int):
    """Выдает номера банковских карт в формате (XXXX XXXX XXXX XXXX), где (X) — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."""
    if len(str(start)) > 16 or len(str(end)) > 16:
        raise ValueError("Динна номера не может быть больше 16 символов")

    for number in range(start, end + 1):
        # Форматирую через f-строки 0 это заполнитель, общее поле 16, d подставить целое число
        num_str = f"{number:016d}"

        groups = [num_str[i : i + 4] for i in range(0, 16, 4)]
        yield " ".join(groups)
