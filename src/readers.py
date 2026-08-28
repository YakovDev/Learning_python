import csv
from pathlib import Path
from typing import Any, cast

import pandas as pd

# Поднимаемся на два уровня
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Пути к файлам данных
CSV_PATH = DATA_DIR / "transactions.csv"
EXCEL_PATH = DATA_DIR / "transactions_excel.xlsx"


def reader_csv_file(file: Path | str) -> list[dict[str, Any]]:
    """Принимает на вход путь к файлу .csv и возвращает список словарей.
    Функция определяет разделитель по первой строке
    """

    try:
        with open(file, encoding="utf-8") as f:
            # Определяем разделитель по первой строке
            first_line = f.readline()
            f.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(first_line).delimiter
            reader = csv.DictReader(f, delimiter=delimiter)
            row_list = []
            for row in reader:
                amount = row.get("amount")
                currency = row.get("currency")
                currency_name = row.get("currency_name")
                currency_code = row.get("currency_code")
                name = currency_name or currency
                code = currency_code or currency
                row["operationAmount"] = {"amount": amount, "currency": {"name": name, "code": code}}
                # Удаляем плоские поля, чтобы не мешали
                for key in ["amount", "currency", "currency_name", "currency_code"]:
                    row.pop(key, None)
                row_list.append(row)
        return row_list
    except (FileNotFoundError, csv.Error):
        return []


def reader_xls_file(file: Path | str) -> list[dict[str, Any]]:
    """Принимает на вход путь к файлу .xlsx и возвращает список словарей"""
    try:
        df = pd.read_excel(file)
        result = df.to_dict("records")
        for row in result:
            amount = row.pop("amount", None)
            currency = row.pop("currency", None)
            currency_name = row.pop("currency_name", None)
            currency_code = row.pop("currency_code", None)
            name = currency_name or currency
            code = currency_code or currency
            row["operationAmount"] = {"amount": amount, "currency": {"name": name, "code": code}}
        return cast(list[dict[str, Any]], result)
    except FileNotFoundError:
        return []
