import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")

if not API_KEY:
    raise ValueError("EXCHANGE_RATES_API_KEY not set")
CONVERT_URL = "https://api.apilayer.com/exchangerates_data/convert"


def external_api(transaction: dict) -> float:
    """
    Функция принимает словарь транзакции, извлекает из него сумму и код валюты.
    Если валюта уже RUB, возвращает сумму без изменений.
    Для USD, EUR и других валют выполняет HTTP-запрос к внешнему API,
    получает текущий курс к рублю и конвертирует сумму.
    """
    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if amount is None or currency is None:
        return 0.0

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return 0.0

    if currency == "RUB":
        return round(amount, 2)

    params = {"to": "RUB", "from": currency, "amount": amount}
    headers = {"apikey": API_KEY}
    try:
        response = requests.get(CONVERT_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        rate = data.get("info", {}).get("rate")

        if rate is None:
            return 0.0

        return round(amount * float(rate), 2)
    except requests.exceptions.HTTPError:
        return 0.0
