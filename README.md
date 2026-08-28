# Виджет банковских операций

Виджет для отображения и обработки информации о банковских операциях клиента.  
Проект включает как библиотеку утилит, так и готовое интерактивное консольное приложение.

### 🔧 Библиотека утилит предоставляет:

- маскировку номеров банковских карт и счетов;
- преобразование даты в читаемый формат;
- фильтрацию и сортировку списка операций по статусу и дате;
- генерацию номеров карт и итераторов по транзакциям;
- поиск по описанию и подсчёт категорий операций;
- загрузку транзакций из **JSON**, **CSV** и **Excel**;
- конвертацию валют в рубли через внешний API;
- автоматическое логирование выполнения функций в консоль или файл;
- модульные тесты с покрытием 100%.

### 🖥️ Консольное приложение (`main.py`) позволяет:

- выбрать источник данных (JSON, CSV, Excel);
- отфильтровать транзакции по статусу (`EXECUTED`, `CANCELED`, `PENDING`);
- отсортировать по дате (возрастание/убывание);
- отобрать только рублёвые операции;
- выполнить поиск по ключевому слову в описании;
- вывести итоговый список с маскировкой счетов и дат, а также показать топ‑5 категорий операций.

---

## 📁 Структура проекта
```
project_root/
├──  main.py            # Главный исполняемый модуль
├── .gitignore          # Исключения для Git (виртуальное окружение, кеши, отчёты)
├── .flake8             # Конфигурация линтера Flake8
├── README.md           # Описание проекта
├── logs/               # Директория с данными
│   ├── masks.log # Логи masks.py
│   └── utils.logs # Логи utils.py
├── data/               # Директория с данными
│   ├── operations.json # Пример файла с транзакциями в формате json
│   ├── transactions.csv # Пример файла с транзакциями в формате csv
│   └── transactions_excel.xlsx # Пример файла с транзакциями в формате xlsx
├── src/                # Исходный код
│   ├── __init__.py     # Делает папку пакетом
│   ├── masks.py        # Функции маскировки номеров карт/счетов
│   ├── processing.py   # Фильтрация и сортировка операций
│   ├── generator.py    # Генераторы и итераторы по транзакциям
│   ├── search.py       # Поиск по описанию и подсчёт категорий 
│   ├── utils.py        # Загрузка транзакций из JSON
│   ├── decorators.py   # Декоратор логирования
│   ├── widget.py       # Основной виджет (маскировка + дата)
│   ├── external_api.py # Конвертация валют через внешний API
│   └── readers.py      # Чтение транзакций из CSV и Excel
└── tests/              # Тесты (pytest)
    ├── init.py
    ├── conftest.py # Общие фикстуры
    ├── test_masks.py
    ├── test_processing.py
    ├── test_generator.py
    ├── test_widget.py
    ├── test_decorator.py
    ├── test_utils.py
    ├── test_external_api.py
    ├── test_readers.py
    └── test_search.py
```
---
## 🚀 Установка

### Требования
- **Python 3.8** или выше
- Менеджер пакетов [Poetry](https://python-poetry.org/) (рекомендуется) или `pip`

### Установка через Poetry (рекомендовано)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/YakovDev/Learning_python
   cd widget-bank-operations
   ```
2. Установите зависимости и создайте виртуальное окружение:
   ```bash
   poetry install
   pip init
   ```
3. Активируйте окружение:
   ```bash
   poetry shell # Poetry
   venv\Scripts\Activate.ps1 # PowerShell
   source venv/bin/activate # Linux / Mac
   ```
4. Создайте файл `.env` в корне проекта (скопируйте из `.env.example`) и добавьте ваш API-ключ:
   ```
   EXCHANGE_RATES_API_KEY=ваш_ключ_api
   ```
---
## 📦 Описание модулей
### `main.py`
Главный исполняемый модуль, запускающий интерактивное консольное приложение.
Он не импортируется как библиотека, а запускается напрямую:
```bash
   python main.py
   ```
Приложение последовательно:

1. Предлагает выбрать источник данных (JSON, CSV или Excel).

2. Фильтрует транзакции по статусу (EXECUTED, CANCELED, PENDING).

3. Сортирует по дате (по возрастанию или убыванию).

4. Опционально оставляет только рублёвые операции.

5. Позволяет отфильтровать по ключевому слову в описании.

6. Выводит итоговый список с маскировкой счетов и дат, а также топ‑5 категорий операций.


---


### `masks.py`
Содержит функции для маскировки номеров банковских карт и счетов с логированием в `logs/masks.log`.
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
  

---


### `get_date(date_string: str) -> str`  
  Принимает строку с датой в ISO-формате (`"2024-03-11T02:26:18.671407"`) и возвращает дату в формате `"ДД.ММ.ГГГГ"`
  ```python
   from src.widget import get_date

    get_date("2024-03-11T02:26:18.671407")  # "11.03.2024"
    get_date("некорректная дата")           # "Дата неизвестна"
    
  ```


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
  

---


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


---


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


### `decorators.py`

Содержит декоратор `log` для автоматического логирования вызовов функций.

- `log(filename: str = "") -> Callable`  
  Декоратор, который логирует начало, результат/ошибку и завершение выполнения функции.  
  Если передан `filename` – логи записываются в файл (режим `"a+"`), иначе – выводятся в консоль.

  Пример:
  ```python
  from src.decorators import log

  @log()  # вывод в консоль
  def add(a, b):
      return a + b

  @log(filename="app.log")  # запись в файл
  def divide(x, y):
      if y == 0:
          raise ValueError("Деление на ноль")
      return x / y
  ```
  

---


### `search.py`
Содержит функции для поиска по описанию и подсчёта категорий транзакций.

- `process_bank_search(data: list[dict], search_string: str) -> list[dict]`

- Фильтрует список транзакций, оставляя только те, у которых поле description содержит искомую подстроку (регистронезависимо).
Если search_string пустая, возвращает исходный список.

  ```python
  from src.search import process_bank_search

  transactions = [
  {"id": 1, "description": "Перевод в кафе"},
  {"id": 2, "description": "Покупка в магазине"},
  {"id": 3, "description": "Перевод другу"}
  ]
  process_bank_search(transactions, "перевод")  # вернёт транзакции с id 1 и 3
  ```
  `count_operations_by_category(data: list[dict], categories: list[str]) -> dict[str, int]`
-   Подсчитывает, сколько транзакций из списка относятся к каждой из переданных категорий (поиск по описанию).
  Возвращает словарь {категория: количество}.
  
    ```python
    from src.search import count_operations_by_category

    transactions = [
    {"description": "Перевод в кафе"},
    {"description": "Покупка в магазине"},
    {"description": "Перевод другу"}
    ]
    count_operations_by_category(transactions, ["Перевод", "Покупка"])
    # {"Перевод": 2, "Покупка": 1}
    ```


---


### `external_api.py`
Содержит функцию для конвертации суммы транзакции в рубли с использованием внешнего API [Exchange Rates Data API](https://apilayer.com/exchangerates_data-api).

- **Переменные окружения**  
  Для работы требуется переменная `EXCHANGE_RATES_API_KEY`, которая должна быть задана в файле `.env`.  
  Если ключ отсутствует, при импорте модуля выбрасывается `ValueError`.

- `external_api(transaction: dict) -> float`  
  Принимает словарь транзакции с ключами `amount` (сумма) и `currency` (код валюты).  
  Если валюта `"RUB"` – возвращает сумму без изменений.  
  Для других валют отправляет запрос к API и конвертирует сумму по текущему курсу к рублю.  
  В случае ошибок (сеть, HTTP-статус, отсутствие курса) возвращает `0.0`.

  *Пример:*
  ```python
  from src.external_api import external_api

  tx = {"amount": 100, "currency": "USD"}
  rub_amount = external_api(tx)   # например, 9125.00
  ```
  

---


### `readers.py`
Содержит функции для чтения транзакций из CSV и Excel-файлов с нормализацией структуры.

- `reader_csv_file(file_path: Path | str) -> list[dict]`  
Принимает путь к CSV-файлу, автоматически определяет разделитель, читает данные и преобразует плоские поля (amount, currency, currency_name, currency_code) во вложенный словарь operationAmount.
В случае ошибки возвращает пустой список
  ```python
  from src.readers import reader_csv_file

  transactions = reader_csv_file("data/transactions.csv")
  # каждый элемент будет содержать ключ "operationAmount" с вложенными "amount" и "currency"
  ```

- `reader_xls_file(file_path: Path | str) -> list[dict]`  
Аналогично для Excel-файлов (.xlsx) с использованием pandas.
Возвращает список словарей с нормализованной структурой.

  *Пример:*
  ```python
  from src.readers import reader_xls_file
  transactions = reader_xls_file("data/transactions_excel.xlsx")
  ```
  
---

### `utils.py`
Содержит функцию для загрузки транзакций из JSON-файла с логированием в logs/utils.log.
- `load_transactions_json(file_path: str) -> list[dict]`
  - Принимает путь к JSON-файлу, если файл существует и содержит список словарей, возвращает этот список.
В случае ошибок (файл не найден, некорректный JSON, данные не список) возвращает пустой список.
  *Пример:*
  ```python
    from src.utils import load_transactions_json

    transactions = load_transactions_json("data/operations.json")
    # если всё ок, получим список транзакций, иначе []
    ```

  ```

---
## 🧪 Тестирование

Для обеспечения корректности работы всех функций в проекте написаны **модульные тесты** с использованием фреймворка `pytest`. Тесты покрывают:

- все функции маскировки (`test_masks.py`);
- фильтрацию и сортировку операций (`test_processing.py`);
- основной виджет и преобразование даты (`test_widget.py`);
- генераторы и итераторы по транзакциям и картам (`test_generator.py`);
- декоратор логирования (`test_decorator.py`);
- загрузку из JSON (`test_utils.py`);
- конвертацию валют через внешний API (`test_external_api.py`);
- чтение из CSV и Excel (`test_readers.py`);
- поиск по описанию и подсчёт категорий (`test_search.py`).

Общее покрытие кода тестами составляет **100%** (проверено с помощью `pytest-cov`).

### Установка зависимостей для тестирования

Установите `pytest` и `pytest-cov` (желательно в виртуальном окружении):

```bash
    poetry add pytest pytest-cov
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
| src\decorators.py    | 23         | 0       | 0        | 100%     |
| src\external_api.py  | 32         | 0       | 0        | 100%     |
| src\generator.py     | 17         | 0       | 0        | 100%     |
| src\masks.py         | 37         | 0       | 0        | 100%     |
| src\processing.py    | 11         | 0       | 0        | 100%     |
| src\readers.py       | 46         | 0       | 0        | 100%     |
| src\search.py        | 22         | 0       | 0        | 100%     |
| src\utils.py         | 30         | 0       | 0        | 100%     |
| src\widget.py        | 19         | 0       | 0        | 100%     |
| **Total**            | 237        | 0       | 0        | 100%     |
```
---
## Пример использования
```python
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.generator import filter_by_currency, transaction_descriptions, card_number_generator
from src.decorators import log
from src.utils import load_transactions_json
from src.external_api import external_api
from src.readers import reader_csv_file, reader_xls_file
from src.search import process_bank_search, count_operations_by_category

# 1. Маскировка
print(mask_account_card("Maestro 7000792289606361"))
# Maestro 7000 79** **** 6361

# 2. Преобразование даты
print(get_date("2024-03-11T02:26:18.671407"))
# 11.03.2024

# 3. Фильтрация и сортировка
data = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "state": "CANCELED", "date": "2024-02-10T14:12:00.000000"},
    {"id": 3, "state": "EXECUTED", "date": "2024-01-05T09:30:00.000000"}
]
filtered = filter_by_state(data, "EXECUTED")
sorted_data = sort_by_date(filtered)
print(sorted_data)

# 4. Генераторы для транзакций
transactions = [
    {"id": 1, "description": "Оплата", "operationAmount": {"amount": "100.50", "currency": {"name": "USD"}}},
    {"id": 2, "description": "Перевод", "operationAmount": {"amount": "250.00", "currency": {"name": "EUR"}}}
]
for t in filter_by_currency(transactions, "USD"):
    print(t["id"])  # 1
for desc in transaction_descriptions(transactions):
    print(desc)

# 5. Генерация карт
for card in card_number_generator(1, 3):
    print(card)

# 6. Загрузка из JSON (исправлено имя функции)
loaded = load_transactions_json("data/operations.json")
print(f"Загружено {len(loaded)} транзакций")

# 7. Загрузка из CSV и Excel (новое)
csv_data = reader_csv_file("data/transactions.csv")
xlsx_data = reader_xls_file("data/transactions_excel.xlsx")
print(f"CSV: {len(csv_data)}, Excel: {len(xlsx_data)}")

# 8. Поиск и категории (новое)
found = process_bank_search(loaded, "перевод")
print(f"Найдено {len(found)} транзакций с 'перевод'")
cats = count_operations_by_category(loaded, ["Перевод", "Покупка"])
print(cats)

# 9. Конвертация валюты
tx = {"amount": 100, "currency": "USD"}
rub = external_api(tx)
print(f"100 USD = {rub} RUB")

# 10. Логирование
@log()
def multiply(a, b):
    return a * b

print(multiply(2, 3))
```
---
## 🛠 Технологии
- **Python 3.8+** – язык программирования.
- **Стандартная библиотека:**  
  - `re` – регулярные выражения для маскировки.  
  - `datetime` – работа с датами и временем.  
  - `json` – чтение/запись данных в формате JSON.  
  - `functools` – сохранение метаданных через `@wraps`.  
  - `typing` – аннотации типов для читаемости кода.  
  - `logging` – базовое логирование (используется в декораторе).
- **Внешние библиотеки:**  
  - `requests` – библиотека для выполнения HTTP-запросов (используется в `external_api.py` для обращения к API конвертации валют).  
  - `python-dotenv` – загрузка переменных окружения из файла `.env` (скрывает чувствительные данные, такие как API-ключи).
- **Тестирование:**  
  - `pytest` – фреймворк для модульных тестов.  
  - `pytest-cov` – плагин для измерения покрытия кода.  
  - `requests-mock` – для мокирования HTTP-запросов и окружения в тестах.
- **Инструменты управления зависимостями:**  
  - `poetry` – управление зависимостями и виртуальным окружением.
- **Работа с данными:**  
  - `pandas` – чтение Excel-файлов.  
  - `openpyxl` – движок для работы с `.xlsx`.