import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "input_card,expected",
    [
        (1234567891012131, "1234 56** **** 2131"),
        ("1234567891012131"[::-1], "1312 10** **** 4321"),
    ],
)
def test_get_mask_card_number(input_card: int | str, expected: str) -> None:
    assert get_mask_card_number(input_card) == expected


def test_get_mask_card_number_error() -> None:
    assert get_mask_card_number("") == "Номер должен быть равен 16 или введите числа"


# Тестирование правильности маскирования номера счета.
# Проверка работы функции с различными форматами и длинами номеров счетов.
# Проверка, что функция корректно обрабатывает входные данные, где номер счета меньше ожидаемой длины.
def test_get_mask_account() -> None:
    assert get_mask_account("44444") == "**4444"
    assert get_mask_account("") == "Ошибка ввода"
