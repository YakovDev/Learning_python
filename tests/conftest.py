import csv

import pandas as pd
import pytest


@pytest.fixture()
def _filter_by_state():
    return [
        {"id": 3, "state": "", "date": "2025-12-15T11:30:45.123Z"},
        {"id": 5, "state": "CANCELED", "date": "2025-04-15T11:30:45.123Z"},
        {"id": 2, "state": "PENDING", "date": "2025-03-15T11:30:45.123Z"},
        {"id": 1, "state": "EXECUTED", "date": "2025-02-15T11:30:45.123Z"},
    ]


@pytest.fixture
def transactions():
    """Фикстура с набором транзакций"""
    return [
        {
            "id": 1,
            "description": "Перевод в кафе",
            "operationAmount": {"amount": "100.50", "currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 2,
            "description": "Покупка в магазине",
            "operationAmount": {"amount": "250.00", "currency": {"name": "EUR", "code": "EUR"}},
        },
        {
            "id": 3,
            "description": "Оплата подписки",
            "operationAmount": {"amount": "9.99", "currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 4,
            "description": "",  # пустое описание
            "operationAmount": {"amount": "50.00", "currency": {"name": "RUB", "code": "RUB"}},
        },
        {
            "id": 5,
            "description": None,  # отсутствует описание
            "operationAmount": {"amount": "30.00", "currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 6,
            # нет поля operationAmount – транзакция без валюты
            "description": "Без валюты",
        },
        {
            "id": 7,
            "description": "Перевод другу",
            "operationAmount": {
                "amount": "200.00"
                # нет вложенного "currency" – валюта отсутствует
            },
        },
    ]


@pytest.fixture
def rub_transaction():
    """Фикстура для транзакции в рублях"""
    return {"amount": 100.50, "currency": "RUB"}


@pytest.fixture
def usd_transaction():
    """Фикстура для транзакции в долларах"""
    return {"amount": 50.00, "currency": "USD"}


@pytest.fixture
def csv_file(tmp_path):
    """Создаёт временный CSV-файл с тестовыми данными."""
    data = [
        {"id": "1", "amount": "100.50", "currency": "USD"},
        {"id": "2", "amount": "200.00", "currency": "EUR"},
        {"id": "3", "amount": "50.25", "currency": "USD"},
    ]
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return file_path


@pytest.fixture
def excel_file(tmp_path):
    """Создаёт временный Excel-файл с тестовыми данными."""
    data = pd.DataFrame(
        [
            {"id": 1, "amount": 100.50, "currency": "USD"},
            {"id": 2, "amount": 200.00, "currency": "EUR"},
            {"id": 3, "amount": 50.25, "currency": "USD"},
        ]
    )
    file_path = tmp_path / "test.xlsx"
    data.to_excel(file_path, index=False)
    return file_path


@pytest.fixture
def csv_empty_file(tmp_path):
    """Создаёт CSV-файл только с заголовками, без строк."""
    file_path = tmp_path / "empty.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "amount", "currency"])
        writer.writeheader()
    return file_path


@pytest.fixture
def excel_empty_file(tmp_path):
    """Создаёт Excel-файл только с заголовками, без строк."""
    data = pd.DataFrame(columns=["id", "amount", "currency"])
    file_path = tmp_path / "empty.xlsx"
    data.to_excel(file_path, index=False)
    return file_path
