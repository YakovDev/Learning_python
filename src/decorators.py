from functools import wraps
from typing import Any, Callable


def log(filename: str = "") -> Callable:
    """
    Декоратор log для автоматического логирования вызовов функций.
    Декоратор, который логирует начало, результат/ошибку и завершение выполнения функции.
    Если передан `filename` – логи записываются в файл (режим `"a+"`), иначе – выводятся в консоль.
    """

    def inner(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            def message_log(message: str) -> None:

                if not filename:
                    print(f"{message}\n {func.__name__}")
                else:
                    with open(filename, "a+", encoding="utf-8") as file:
                        file.write(f"{message}\n {func.__name__}")

            message_log(f"Начало выполнения функции {func.__name__}")
            try:
                result = func(*args, **kwargs)
                message_log(
                    f"Успешно! Результат: {result}\n"
                    f"Позиционные аргументы: {args}\n"
                    f"Именованные аргументы: {kwargs}"
                )
                message_log(f"Конец выполнения функции {func.__name__}")
                return result
            except Exception as e:
                message_log(
                    f"Ошибка {type(e).__name__}\n"
                    f"Позиционные аргументы: {args}\n"
                    f"Именованные аргументы: {kwargs}"
                )
                message_log(f"Конец выполнения функции {func.__name__} с ошибкой")
                raise

        return wrapper

    return inner
