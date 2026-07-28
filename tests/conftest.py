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
