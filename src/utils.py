import json
import logging
import os
from pathlib import Path

# Определил путь до файла с операциями по счетам
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JSON_PATH = DATA_DIR / "operations.json"

# Определяю корень проекта (папка, где находится этот файл, поднимаемся на уровень выше)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # если файл лежит в src/, корень — на уровень выше

logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
log_path = os.path.join(logs_dir, "utils.log")  # отдельный файл для модуля

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_path,
    filemode="w",
    force=True,
)
logger_load_transactions = logging.getLogger("Load_Transactions.utils")


def load_transactions_json(file_path: str) -> list[dict]:
    """
    Принимает путь до файла читает файл если файл список то возвращает его.
    Если файл пустой вернет пустой список.
    Если путь будет указан неверно тоже вернет пустой список.
    """
    logger_load_transactions.info("Начало работы")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions = json.load(f)
            if isinstance(transactions, list):
                logger_load_transactions.info("Успешно!")
                return transactions
            logger_load_transactions.error("Данные в файле не являются списком")
            return []
    except FileNotFoundError:
        logger_load_transactions.error("Файл не найден")
        return []
    except json.JSONDecodeError:
        logger_load_transactions.error("Некорректный JSON в файле")
        return []
