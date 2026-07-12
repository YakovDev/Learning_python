import pytest


@pytest.fixture()
def _filter_by_state():
    return [
        {"id": 3, "state": "", "date": "2025-12-15T11:30:45.123Z"},
        {"id": 5, "state": "CANCELED", "date": "2025-04-15T11:30:45.123Z"},
        {"id": 2, "state": "PENDING", "date": "2025-03-15T11:30:45.123Z"},
        {"id": 1, "state": "EXECUTED", "date": "2025-02-15T11:30:45.123Z"},
    ]
