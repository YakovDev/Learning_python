from typing import Any
import sys
from typing import Any
from unittest.mock import Mock, patch

import pytest
import requests


def test_external_api_no_api_call(rub_transaction: dict[str, Any]) -> None:
    """Проверка конвертации RUB (без запроса к API)."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        result = external_api(rub_transaction)
        assert result == 100.50


def test_external_api_http_error(usd_transaction: dict[str, Any]) -> None:
    """Ошибка HTTP 404 → возврат 0.0."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        with patch("src.external_api.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
            mock_get.return_value = mock_response

            result = external_api(usd_transaction)
            assert result == 0.0


def test_external_api_missing_rate(usd_transaction: dict[str, Any]) -> None:
    """Ответ API без поля rate → возврат 0.0."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        with patch("src.external_api.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"info": {}}  # нет rate
            mock_get.return_value = mock_response

            result = external_api(usd_transaction)
            assert result == 0.0


def test_external_api_invalid_data() -> None:
    """Некорректные данные транзакции → возврат 0.0."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        assert external_api({"amount": "abc", "currency": "USD"}) == 0.0
        assert external_api({}) == 0.0
        assert external_api({"amount": 100}) == 0.0  # нет currency


def test_external_api_success(usd_transaction: dict[str, Any]) -> None:
    """Успешная конвертация USD → RUB с проверкой вызова requests.get."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        with patch("src.external_api.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"info": {"rate": 91.25}}
            mock_get.return_value = mock_response

            result = external_api(usd_transaction)

            mock_get.assert_called_once_with(
                "https://api.apilayer.com/exchangerates_data/convert",
                params={"to": "RUB", "from": "USD", "amount": 50.00},
                headers={"apikey": "Test_aip_key"},
                timeout=10,
            )
            assert result == 4562.50


def test_if_not_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Так как если просто удалить API_key не удается потому что os.getevn находит папку и
    сразу возвращает переменную в строй нужно было через патч указать возвращаемое значение по
    умолчанию None и уже после удалить ключ и импортировать модуль для проверки
    """

    with patch("src.external_api.os.getenv", return_value=None):
        if "src.external_api" in sys.modules:
            del sys.modules["src.external_api"]
        with pytest.raises(ValueError):
            import src.external_api
