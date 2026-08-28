import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список транзакций по наличию строки поиска в поле 'description'.

    Аргументы:
        data (List[Dict[str, Any]]): Список словарей с данными о банковских операциях.
        search (str): Строка для поиска (регистронезависимо).

    Возвращает:
        List[Dict[str, Any]]: Список транзакций, у которых поле 'description' содержит искомую строку.
    """

    if search == "":
        return data

    pattern = re.compile(search, flags=re.IGNORECASE)
    result = []
    for item in data:
        description = item.get("description")
        if pattern.search(str(description)):
            result.append(item)
    return result


def count_operations_by_category(data: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество транзакций, относящихся к каждой из указанных категорий.
    """
    result = {category: 0 for category in categories}

    for item in data:
        description = str(item.get("description", ""))
        if not description:
            continue

        for category in categories:
            if re.search(re.escape(category), description, flags=re.IGNORECASE):
                result[category] += 1
                break

    return result
