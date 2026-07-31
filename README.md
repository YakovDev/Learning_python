# Виджет банковских операций
Виджет для отображения информации о банковских операциях клиента.  
Проект содержит набор утилит для:
- маскировки номеров банковских карт и счетов;
- преобразования даты в читаемый формат;
- фильтрации и сортировки списка операций по статусу и дате;
- генерации номеров карт и итераторов по транзакциям.
---
## 📁 Структура проекта
```
.
├── .gitignore          # Исключаемые файлы и папки
├── .flake8             # Конфигурация линтера Flake8
├── README.md           # Описание проекта
├── src/                # Исходный код
│   ├── __init__.py
│   ├── masks.py        # Функции маскировки
│   ├── processing.py   # Фильтрация и сортировка операций
│   ├── generator.py    # Генераторы и итераторы по транзакциям
│   └── widget.py       # Основной виджет (маскировка + дата)
└── tests/              # Тесты (pytest)
    ├── __init__.py
    ├── conftest.py        # Фикстуры для тестов
    ├── test_masks.py      # Тесты для masks.py
    ├── test_processing.py # Тесты для processing.py
    ├── test_generator.py  # Тесты для generator.py
    └── test_widget.py     # Тесты для widget.py
```
---
## 🚀 Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-username/widget-bank-operations.git
   cd widget-bank-operations
   ```
2. Убедитесь, что установлен Python версии **3.8** или выше.
3. (Опционально) Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
Проект не требует внешних зависимостей — используется только стандартная библиотека Python.
---
## 📦 Описание модулей
### `masks.py`
Содержит функции для маскировки номеров карт и счетов.
- `get_mask_card_number(card_number: str | int) -> str`  
  Принимает номер карты (16 цифр) и возвращает его в замаскированном формате:  
  `XXXX XX** **** XXXX`  
  *(например, `7000 79** **** 6361`)*
- `get_mask_account(account_number: str) -> str`  
  Принимает номер счёта (любой длины) и возвращает только последние 4 цифры с двумя звёздочками:  
  `**XXXX`  
  *(например, `**4305`)*
---
### `widget.py`
Содержит основной функционал виджета.
- `mask_account_card(card_info: str | int) -> str`  
  Принимает строку с типом и номером карты или счёта (например,  
  `"Visa Platinum 7000792289606361"` или `"Счет 73654108430135874305"`).  
  Автоматически определяет тип и возвращает строку с замаскированным номером.  
  - Для карт использует `get_mask_card_number`  
  - Для счетов — `get_mask_account`  
  *Пример:*
  ```python
  mask_account_card("Visa Platinum 7000792289606361")
  # -> "Visa Platinum 7000 79** **** 6361"
  
  mask_account_card("Счет 73654108430135874305")
  # -> "Счет **4305"
  ```
- `get_date(date_string: str) -> str`  
  Принимает строку с датой в ISO-формате (`"2024-03-11T02:26:18.671407"`) и возвращает дату в формате `"ДД.ММ.ГГГГ"` (например, `"11.03.2024"`).
---
### `processing.py`
Содержит функции для обработки списка операций.
- `filter_by_state(list_of_dict: list[dict], state: str = "EXECUTED") -> list[dict]`  
  Фильтрует список словарей по значению ключа `state`.  
  Возвращает новый список, содержащий только словари с указанным статусом.
  *Пример:*
  ```python
  operations = [
      {"id": 1, "state": "EXECUTED", "date": "..."},
      {"id": 2, "state": "CANCELED", "date": "..."}
  ]
  filter_by_state(operations, "EXECUTED")  # вернёт только первую операцию
  ```
- `sort_by_date(list_of_dict: list[dict], reverse: bool = True) -> list[dict]`  
  Сортирует список операций по дате (ключ `date`).  
  По умолчанию сортировка по убыванию (от новых к старым).  
  Возвращает **новый** отсортированный список.
---
### `generator.py`
Содержит генераторы и итераторы для работы с транзакциями и номерами карт.
- `filter_by_currency(transactions: list[dict], currency: str)`  
  Принимает список словарей с транзакциями и код валюты (например, `"USD"`).  
  Возвращает итератор, который поочерёдно выдаёт только те транзакции, у которых валюта операции соответствует заданной.  
  Значение валюты извлекается по пути `operationAmount.currency.name`.
  *Пример:*
  ```python
  transactions = [
      {"id": 1, "operationAmount": {"amount": "100.50", "currency": {"name": "USD", "code": "USD"}}},
      {"id": 2, "operationAmount": {"amount": "250.00", "currency": {"name": "EUR", "code": "EUR"}}},
      {"id": 3, "operationAmount": {"amount": "9.99", "currency": {"name": "USD", "code": "USD"}}}
  ]
  usd_transactions = filter_by_currency(transactions, "USD")
  for t in usd_transactions:
      print(t["id"])  # 1, 3
  ```
- `transaction_descriptions(transactions: list[dict])`  
  Генератор, который принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.  
  Если описание отсутствует — возвращает пустую строку `""`, если поле `description` равно `None` — возвращает `None`.
  *Пример:*
  ```python
  transactions = [
      {"id": 1, "description": "Перевод в кафе"},
      {"id": 2, "description": "Покупка в магазине"},
      {"id": 3, "description": None}
  ]
  for desc in transaction_descriptions(transactions):
      print(desc)
  # "Перевод в кафе"
  # "Покупка в магазине"
  # None
  ```
- `card_number_generator(start: int, end: int)`  
  Генератор, который выдаёт номера банковских карт в формате `XXXX XXXX XXXX XXXX` в заданном диапазоне от `start` до `end` включительно.  
  Номера дополняются ведущими нулями до 16 цифр.  
  Если `start > end` — генератор не выдаёт ни одного значения (пустой итератор).  
  При передаче числа длиннее 16 цифр выбрасывает `ValueError`.
  *Пример:*
  ```python
  list(card_number_generator(1, 3))
  # ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
  list(card_number_generator(3, 1))
  # [] (пустой список, start > end)
  ```
---
## 🧪 Тестирование
Для обеспечения корректности работы всех функций в проекте написаны **модульные тесты** с использованием фреймворка `pytest`. Тесты покрывают:
- все функции маскировки (`test_masks.py`);
- фильтрацию и сортировку операций (`test_processing.py`);
- основной виджет и преобразование даты (`test_widget.py`);
- генераторы и итераторы по транзакциям и картам (`test_generator.py`).
Общее покрытие кода тестами составляет **100%** (проверено с помощью `pytest-cov`).
### Установка зависимостей для тестирования
Установите `pytest` и `pytest-cov` (желательно в виртуальном окружении):
```bash
pip install pytest pytest-cov
```
### Запуск тестов
Выполните команду из корневой директории проекта:
```bash
pytest 
```
Для получения отчёта о покрытии выполните:
```bash
pytest --cov=src tests/
```
Или с генерацией HTML-отчёта:
```bash
pytest --cov=src --cov-report=html
```
После этого отчёт будет доступен в папке `htmlcov/index.html`.
### Пример вывода покрытия
```
| File                 | statements | missing | excluded | coverage |
|----------------------|------------|---------|----------|----------|
| src\__init__.py      | 0          | 0       | 0        | 100%     |
| src\masks.py         | 12         | 0       | 0        | 100%     |
| src\processing.py    | 11         | 0       | 0        | 100%     |
| src\generator.py     | 18         | 0       | 0        | 100%     |
| src\widget.py        | 18         | 0       | 0        | 100%     |
| **Total**            | 59         | 0       | 0        | 100%     |
```
---
## Пример использования
```python
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.generator import filter_by_currency, transaction_descriptions, card_number_generator
# Маскировка
print(mask_account_card("Maestro 7000792289606361"))
# Maestro 7000 79** **** 6361
# Преобразование даты
print(get_date("2024-03-11T02:26:18.671407"))
# 11.03.2024
# Фильтрация и сортировка
data = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "state": "CANCELED", "date": "2024-02-10T14:12:00.000000"},
    {"id": 3, "state": "EXECUTED", "date": "2024-01-05T09:30:00.000000"}
]
filtered = filter_by_state(data, "EXECUTED")
sorted_data = sort_by_date(filtered)
print(sorted_data)
# Фильтрация по валюте
transactions = [
    {"id": 1, "operationAmount": {"amount": "100.50", "currency": {"name": "USD", "code": "USD"}}},
    {"id": 2, "operationAmount": {"amount": "250.00", "currency": {"name": "EUR", "code": "EUR"}}},
    {"id": 3, "operationAmount": {"amount": "9.99", "currency": {"name": "USD", "code": "USD"}}}
]
for t in filter_by_currency(transactions, "USD"):
    print(t["id"])
# 1
# 3
# Получение описаний транзакций
for desc in transaction_descriptions(transactions):
    print(desc)
# Генерация номеров карт
for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```
---
## 🛠 Технологии
- Python 3.8+
- Стандартная библиотека:
  - `re` — регулярные выражения
  - `datetime` — работа с датами
- Для тестирования:
  - `pytest` — фреймворк для тестирования
  - `pytest-cov` — плагин для измерения покрытия кода