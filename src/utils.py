import json


def load_transactions(file_path: str) -> list[dict]:
    """
    Принимает путь до файла читает файл если файл список то возвращает его.
    Если файл пустой вернет пустой список.
    Если путь будет указан неверно тоже вернет пустой список.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions = json.load(f)
            if isinstance(transactions, list):
                return transactions
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
