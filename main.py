import sys
from collections import Counter
from src.processing import filter_by_state, sort_by_date
from src.readers import CSV_PATH, EXCEL_PATH, reader_csv_file, reader_xls_file
from src.search import process_bank_search
from src.utils import JSON_PATH, load_transactions_json
from src.widget import get_date, mask_account_card

"""
Главный модуль для запуска приложения обработки банковских транзакций.
Реализует интерактивный диалог с пользователем.

"""


def main() -> None:

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # ---- 1. Выбор источника данных ----
    while True:

        program_1 = input("""Выберите необходимый пункт меню:
            1. Получить информацию о транзакциях из JSON-файла
            2. Получить информацию о транзакциях из CSV-файла
            3. Получить информацию о транзакциях из XLSX-файла\nПользователь: """).strip()

        if program_1 == "1":
            transactions = load_transactions_json(str(JSON_PATH))
            print("Для обработки выбран JSON-файл\n")
            break
        elif program_1 == "2":
            transactions = reader_csv_file(str(CSV_PATH))
            print("Для обработки выбран CSV-файл\n")
            break
        elif program_1 == "3":
            transactions = reader_xls_file(str(EXCEL_PATH))
            print("Для обработки выбран XLSX-файл\n")
            break
        else:
            print(f"Не корректный ввод:{program_1} \nВыберите 1,2 или 3\n\n")
    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    # ---- 2. Фильтрация по статусу ----

    valid_status = ["executed", "canceled", "pending"]

    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )

        if status in valid_status:
            transactions = filter_by_state(transactions, status.upper())
            print(f'Операции отфильтрованы по статусу "{status.upper()}"\n')
            break
        else:
            print(f'Статус операции "{status}" недоступен.\n' "Пожалуйста, выберите из: EXECUTED, CANCELED, PENDING\n")

    if not transactions:
        print("Не найдено ни одной транзакции...")
        return

    # ---- 3. Фильтрация по дате ----

    while True:
        question = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()

        if question in ["да", "нет"]:
            if question == "да":
                while True:
                    order = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
                    if order in ["по возрастанию", "по убыванию"]:
                        reverse = order == "по убыванию"  # True – убывание, False – возрастание
                        transactions = sort_by_date(transactions, reverse)
                        print(f"Операции отсортированы {order}.\n")
                        break
                    else:
                        print("Введите 'по возрастанию' или 'по убыванию'")
            break
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'.")

    # ---- 4. Фильтр по рублёвым транзакциям ----
    while True:
        question = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
        if question in ["да", "нет"]:
            if question == "да":
                transactions = [
                    t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
                ]
            print("Отфильтрованы только рублевые транзакции.\n")
            if not transactions:
                print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
                return
            break
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")

    # ---- 5. Фильтр по слову в описании ----

    while True:
        question = (
            input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
            .strip()
            .lower()
        )
        if question in ["да", "нет"]:
            if question == "да":
                word = input("Введите слово для поиска: ").strip()
                if word:
                    transactions = process_bank_search(transactions, word)
                    print(f"Список транзакций отфильтрован по {word}\n")
                else:
                    print("Поиск не выполнен (пустое слово).")
            break
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # ---- 6. Вывод итогового списка ----
    print("Распечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    descriptions = [t.get("description", "") for t in transactions]
    counter = Counter(descriptions)
    print(f"Аналитика операций: {counter.most_common(5)}\n")

    for t in transactions:
        # Дата
        date_str = t.get("date", "")
        if date_str:
            date_display = get_date(date_str)
        else:
            date_display = "Дата неизвестна"

        # Описание
        description = t.get("description", "Без описания")

        # Откуда и куда (маскируем)
        from_account = t.get("from", "")
        to_account = t.get("to", "")
        from_masked = mask_account_card(from_account) if from_account else "N/A"
        to_masked = mask_account_card(to_account) if to_account else "N/A"

        # Сумма и валюта
        op_amount = t.get("operationAmount", {})
        amount = op_amount.get("amount", "N/A")
        currency = op_amount.get("currency", {}).get("name", "")

        # Вывод в формате из примера
        print(f"{date_display} {description}")
        if from_account and to_account:
            print(f"{from_masked} -> {to_masked}")
        elif from_account:
            print(f"Списание: {from_masked}")
        elif to_account:
            print(f"Зачисление: {to_masked}")
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
