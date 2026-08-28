import json
from pathlib import Path

import pytest

from src.utils import load_transactions_json


def test_load_transactions_valid_file(tmp_path: Path) -> None:
    """Тест: файл с корректным списком словарей."""
    file_path = tmp_path / "valid.json"
    data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = load_transactions_json(str(file_path))
    assert result == data
    assert isinstance(result, list)


def test_load_transactions_empty_file(tmp_path: Path) -> None:
    """Тест: пустой файл -> возвращается пустой список."""
    file_path = tmp_path / "empty.json"
    with open(file_path, "w", encoding="utf-8") as f:
        pass

    result = load_transactions_json(str(file_path))
    assert result == []


def test_load_transactions_invalid_json(tmp_path: Path) -> None:
    """Тест: некорректный JSON -> возвращается пустой список."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("это не json")

    result = load_transactions_json(str(file_path))
    assert result == []


def test_load_transactions_not_a_list(tmp_path: Path) -> None:
    """Тест: JSON не является списком (например, словарь) -> возвращается пустой список."""
    file_path = tmp_path / "dict.json"
    data = {"key": "value"}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = load_transactions_json(str(file_path))
    assert result == []


def test_load_transactions_file_not_found() -> None:
    """Тест: файл не найден -> возвращается пустой список."""
    result = load_transactions_json("non_existent_file.json")
    assert result == []
