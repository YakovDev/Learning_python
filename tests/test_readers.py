from src.readers import reader_xls_file, reader_csv_file
from pathlib import Path

# --- Тесты для CSV ---


def test_reader_csv_file_success(csv_file):
    result = reader_csv_file(csv_file)
    expected = [
        {"id": "1", "amount": "100.50", "currency": "USD"},
        {"id": "2", "amount": "200.00", "currency": "EUR"},
        {"id": "3", "amount": "50.25", "currency": "USD"},
    ]
    assert result == expected


def test_reader_csv_file_not_found():
    non_existent = Path("/non/existent/file.csv")
    result = reader_csv_file(non_existent)
    assert result == []  # Возвращает пустой список при ошибке


def test_reader_csv_file_empty(csv_empty_file):
    result = reader_csv_file(csv_empty_file)
    assert result == []  # Нет строк данных -> пустой список


# --- Тесты для Excel ---


def test_reader_xls_file_success(excel_file):
    result = reader_xls_file(excel_file)
    expected = [
        {"id": 1, "amount": 100.50, "currency": "USD"},
        {"id": 2, "amount": 200.00, "currency": "EUR"},
        {"id": 3, "amount": 50.25, "currency": "USD"},
    ]
    assert result == expected


def test_reader_xls_file_not_found():
    non_existent = Path("/non/existent/file.xlsx")
    result = reader_xls_file(non_existent)
    assert result == []  # Возвращает пустой список при ошибке


def test_reader_xls_file_empty(excel_empty_file):
    result = reader_xls_file(excel_empty_file)
    assert result == []  # Нет строк данных -> пустой список
