import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    ["state", "expected"],
    [
        ("EXECUTED", [{"id": 1, "state": "EXECUTED", "date": "2025-02-15T11:30:45.123Z"}]),
        ("CANCELED", [{"id": 5, "state": "CANCELED", "date": "2025-04-15T11:30:45.123Z"}]),
        ("PENDING", [{"id": 2, "state": "PENDING", "date": "2025-03-15T11:30:45.123Z"}]),
        ("", [{"id": 3, "state": "", "date": "2025-12-15T11:30:45.123Z"}]),
    ],
)
def test_filter_by_state(expected, state, _filter_by_state):
    assert filter_by_state(_filter_by_state, state) == expected


@pytest.mark.parametrize(
    ["procedure", "expected"],
    [
        (True, [3, 5, 2, 1]),
        (False, [1, 2, 5, 3]),
    ],
)
def test_sort_by_date(_filter_by_state, procedure, expected):
    result = sort_by_date(_filter_by_state, procedure)

    list_ids = [data.get("id") for data in result]
    assert list_ids == expected
