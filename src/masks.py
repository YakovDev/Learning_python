def get_mask_card_number(user_input: str | int) -> str:
    """
    Функцию маскировки номера банковской карты
    """

    user_input = str(user_input)
    if len(user_input) != 16 or not user_input.isdigit():
        raise ValueError("Номер должен быть равен 16 или введите числа")

    first_ser = user_input[:4]
    second_ser = user_input[4:8]
    fourth_ser = user_input[12:]

    return f"{first_ser} {second_ser[:2]}** **** {fourth_ser}"


def get_mask_account(numb: str) -> str:
    """
    Принимает номер карты и возвращает последние 4 цифры возможно
    """
    if len(numb) >= 4:
        return f"**{numb[-4:]}"

    raise ValueError("Ошибка ввода")
