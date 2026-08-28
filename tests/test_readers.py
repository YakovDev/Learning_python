from pathlib import Path

from src.readers import reader_csv_file, reader_xls_file

# --- Тесты для CSV ---


def test_reader_csv_file_success(csv_file: Path) -> None:
    result = reader_csv_file(csv_file)
    expected = [
        {
            "id": "1",
            "operationAmount": {
                "amount": "100.50",
                "currency": {"name": "USD", "code": "USD"},
            },
        },
        {"id": "2", "operationAmount": {"amount": "200.00", "currency": {"name": "EUR", "code": "EUR"}}},
        {"id": "3", "operationAmount": {"amount": "50.25", "currency": {"name": "USD", "code": "USD"}}},
    ]
    assert result == expected


def test_reader_csv_file_not_found() -> None:
    non_existent = Path("/non/existent/file.csv")
    result = reader_csv_file(non_existent)
    assert result == []


def test_reader_csv_file_empty(csv_empty_file: Path) -> None:
    result = reader_csv_file(csv_empty_file)
    assert result == []


# --- Тесты для Excel ---


def test_reader_xls_file_success(excel_file: Path) -> None:
    result = reader_xls_file(excel_file)
    expected = [
        {"id": 1, "operationAmount": {"amount": 100.50, "currency": {"name": "USD", "code": "USD"}}},
        {"id": 2, "operationAmount": {"amount": 200.00, "currency": {"name": "EUR", "code": "EUR"}}},
        {"id": 3, "operationAmount": {"amount": 50.25, "currency": {"name": "USD", "code": "USD"}}},
    ]
    assert result == expected


def test_reader_xls_file_not_found() -> None:
    non_existent = Path("/non/existent/file.xlsx")
    result = reader_xls_file(non_existent)
    assert result == []


def test_reader_xls_file_empty(excel_empty_file: Path) -> None:
    result = reader_xls_file(excel_empty_file)
    assert result == []
