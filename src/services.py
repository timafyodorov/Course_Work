import logging
import requests
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()


def get_currency_rates() -> list:
    """Получение курсов валют из API"""
    try:
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            logger.warning(
                "API-ключ для ExchangeRate-API не найден, возвращаются пустые курсы валют"
            )
            return []

        url = "https://api.exchangerate-api.com/v4/latest/RUB"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        currencies = ["USD", "EUR"]
        rates = [
            {"currency": currency, "rate": round(data["rates"][currency], 2)}
            for currency in currencies
            if currency in data["rates"]
        ]
        logger.info("Курсы валют успешно получены")
        return rates

    except requests.RequestException as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка в get_currency_rates: {e}")
        return []


def get_stock_prices() -> list:
    """Получение цен акций из API"""
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            logger.warning(
                "API-ключ для Alpha Vantage не найден, возвращаются пустые цены акций"
            )
            return []

        stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        prices = []
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                price = float(data["Global Quote"]["05. price"])
                prices.append({"stock": stock, "price": round(price, 2)})
            else:
                logger.warning(f"Данные для акции {stock} недоступны")
        logger.info("Цены акций успешно получены")
        return prices

    except requests.RequestException as e:
        logger.error(f"Ошибка при получении цен акций: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка в get_stock_prices: {e}")
        return []


def investment_bank(year_month: str, transactions: list, threshold: float) -> float:
    """Расчёт суммы для инвесткопилки за указанный месяц"""
    try:
        savings = 0.0
        for transaction in transactions:
            date_str = transaction.get("Дата операции", "")
            amount = transaction.get("Сумма операции", 0.0)
            if isinstance(date_str, str) and year_month in date_str:
                if amount < 0:  # Учитываем только расходы
                    rounded_amount = round(-amount / threshold) * threshold
                    savings += rounded_amount + amount
        logger.info(f"Сумма в Инвесткопилке за {year_month}: {savings}")
        return savings
    except Exception as e:
        logger.error(f"Ошибка в investment_bank: {e}")
        return 0.0
