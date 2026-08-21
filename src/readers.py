import csv
from pathlib import Path

import pandas as pd

# Поднимаемся на два уровня
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Пути к файлам данных
CSV_PATH = DATA_DIR / "transactions.csv"
EXCEL_PATH = DATA_DIR / "transactions_excel.xlsx"


def reader_csv_file(file) -> list[dict]:
    """Принимает на вход путь к файлу .csv и возвращает список словарей"""

    try:
        row_list = []
        with open(file) as file_read:
            reader = csv.DictReader(file_read)
            for row in reader:
                row_list.append(row)
            return row_list

    except FileNotFoundError:
        return []


def reader_xls_file(file) -> list[dict]:
    """Принимает на вход путь к файлу .xlsx и возвращает список словарей"""
    try:

        df = pd.read_excel(file)
        result = df.to_dict("records")
        return result

    except FileNotFoundError:
        return []
