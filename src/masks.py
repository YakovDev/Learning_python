import logging
import os

# Определяем корень проекта (папка, где находится этот файл, поднимаемся на уровень выше)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # если файл лежит в src/, корень — на уровень выше
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
log_path = os.path.join(logs_dir, "masks.log")  # отдельный файл для модуля

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_path,
    filemode="w",
    force=True,
)
logger_card_number = logging.getLogger("Card Number.masks")
logger_mask_amount = logging.getLogger("Mask Amount.masks")


def get_mask_card_number(user_input: str | int) -> str:
    """
    Функцию маскировки номера банковской карты
    """
    logger_card_number.info(f"Начало работы функции передано значение: {user_input}")
    try:
        user_input = str(user_input)
        if len(user_input) != 16 or not user_input.isdigit():
            raise ValueError("Номер карты должен содержать ровно 16 цифр")
        first_ser = user_input[:4]
        second_ser = user_input[4:8]
        fourth_ser = user_input[12:]
        logger_card_number.info(f"Успешно!")
        return f"{first_ser} {second_ser[:2]}** **** {fourth_ser}"

    except ValueError as e:
        logger_card_number.error(f"Произошла ошибка: {e}", exc_info=True)
        logger_card_number.warning("Неудача, принудительное завершение!")
        return "Номер должен быть равен 16 или введите числа"

    finally:
        logger_card_number.info("Завершение работы")


def get_mask_account(numb: str) -> str:
    """
    Принимает номер карты и возвращает последние 4 цифры
    """
    logger_mask_amount.info(f"Начало работы переданы значения {numb}")
    try:

        if len(numb) >= 4 and numb.isdigit():
            logger_mask_amount.info("Успешно, Завершение работы!")
            return f"**{numb[-4:]}"
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")
    except Exception as e:
        logger_mask_amount.error(f"Произошла ошибка:{e}", exc_info=True)
        logger_mask_amount.warning("Неудача, принудительное завершение!")
        return "Ошибка ввода"
