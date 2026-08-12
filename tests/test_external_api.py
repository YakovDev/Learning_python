from unittest.mock import patch, Mock

import requests


def test_external_api_no_api_call(rub_transaction):
    """Проверка конвертации RUB (без запроса к API)."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        result = external_api(rub_transaction)
        assert result == 100.50


def test_external_api_http_error(usd_transaction):
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


def test_external_api_missing_rate(usd_transaction):
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


def test_external_api_invalid_data():
    """Некорректные данные транзакции → возврат 0.0."""
    with patch("src.external_api.API_KEY", "test_key"):
        from src.external_api import external_api

        assert external_api({"amount": "abc", "currency": "USD"}) == 0.0
        assert external_api({}) == 0.0
        assert external_api({"amount": 100}) == 0.0  # нет currency


def test_external_api_success(usd_transaction):
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
                headers={"apikey": "test_key"},
                timeout=10,
            )
            assert result == 4562.50
