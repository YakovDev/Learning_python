from functools import wraps
from typing import Callable


def log(filename: str = "") -> Callable:
    def inner(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):

            def message_log(message: str) -> None:

                messages = f"{message}"
                if not filename:
                    print(f"{messages}\n {func.__name__}")
                else:
                    with open(filename, "a+", encoding="utf-8") as file:
                        file.write(f"{messages}\n {func.__name__} ")

            message_log(f"Начало выполнения функции {func.__name__}")
            try:

                result = func(*args, **kwargs)
                message_log(
                    f"Успешно!\nРезультат: {result}\nПозиционные аргументы: {args}\n"
                    f"Именованные аргументы: {kwargs}\n"
                )
                message_log(f"Конец выполнения функции {func.__name__}")
                return result

            except Exception as e:
                message_log(
                    f"Ошибка {type(e).__name__}\n"
                    f"Позиционные аргументы: {args}\n"
                    f"Именованные аргументы: {kwargs}\n"
                )
                raise

        return wrapper

    return inner
