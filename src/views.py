import logging
import pandas as pd
from datetime import datetime
from src.utils import read_transactions
from src.services import get_currency_rates, get_stock_prices

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def homepage_view(date_time_str: str) -> dict:
    """Формирование JSON-ответа для главной страницы"""
    try:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        year_month = date_time.strftime("%Y-%m")

        transactions = read_transactions("data/operations.xlsx")
        if transactions.empty:
            logger.warning("Нет данных о транзакциях")
            return {"error": "Нет данных о транзакциях"}

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
        monthly_transactions = transactions[
            transactions["Дата операции"].dt.strftime("%Y-%m") == year_month
        ]

        cards = []
        if "Номер карты" in monthly_transactions.columns:
            for card in monthly_transactions["Номер карты"].unique():
                card_transactions = monthly_transactions[
                    monthly_transactions["Номер карты"] == card
                ]
                total_spent = card_transactions["Сумма платежа"].sum()
                cashback = (
                    card_transactions["Кэшбэк"].sum()
                    if "Кэшбэк" in card_transactions.columns
                    else 0
                )
                cards.append(
                    {"number": card, "total_spent": total_spent, "cashback": cashback}
                )

        top_transactions = []
        if not monthly_transactions.empty:
            top_transactions = monthly_transactions.nlargest(5, "Сумма платежа")[
                ["Дата операции", "Сумма платежа", "Категория", "Описание"]
            ].to_dict(orient="records")

        currency_rates = get_currency_rates()
        stock_prices = get_stock_prices()

        response = {
            "greeting": "Добрый день",
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }
        logger.info("JSON-ответ для главной страницы успешно сформирован")
        return response

    except Exception as e:
        logger.error(f"Ошибка при формировании JSON-ответа: {e}")
        return {"error": "Внутренняя ошибка сервера"}
