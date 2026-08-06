import pytest

from src.decorators import log


def test_log(capsys):
    my_lambda = log()(lambda a, b: a + b)
    my_lambda(2, 3)
    captured = capsys.readouterr()
    assert (
        captured.out == "Начало выполнения функции <lambda>\n <lambda>\nУспешно!\nРезультат: 5"
        "\nПозиционные аргументы: (2, 3)"
        "\nИменованные аргументы: {}\n\n <lambda>\nКонец выполнения функции <lambda>\n <lambda>\n"
    )


def test_write_to_file(tmp_path):
    log_file = tmp_path / "test.log"
    my_lambda = log(filename=str(log_file))(lambda a, b: a + b)
    result = my_lambda(2, 3)
    assert result == 5
    # Проверяю наличие логов в фале
    chek_in_file = log_file.read_text(encoding="utf-8")
    assert "Начало выполнения функции <lambda>" in chek_in_file
    assert "Успешно!" in chek_in_file
    assert "Результат: 5" in chek_in_file
    assert "Позиционные аргументы: (2, 3)" in chek_in_file
    assert "Именованные аргументы: {}" in chek_in_file
    assert "Конец выполнения функции <lambda>" in chek_in_file


def test_log_error(tmp_path):
    log_file = tmp_path / "test.log"
    my_lambda = log(filename=str(log_file))(lambda a, b: a + b)
    with pytest.raises(TypeError):
        my_lambda(2, "str")
    chek_in_file = log_file.read_text(encoding="utf-8")
    # Проверяю наличие логов в фале
    assert "Ошибка TypeError" in chek_in_file
    assert "Позиционные аргументы:" in chek_in_file
    assert "Именованные аргументы:" in chek_in_file
