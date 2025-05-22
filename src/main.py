import logging
from src.views import homepage_view
from src.services import investment_bank
from src.reports import spending_by_category
from src.utils import read_transactions

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция для демонстрации работы приложения"""
    try:
        date_time_str = "2021-05-20 14:30:00"
        homepage_response = homepage_view(date_time_str)
        logger.info(f"Homepage response: {homepage_response}")

        transactions = [
            {"Дата операции": "2021-05-01", "Сумма операции": -1712.00},
            {"Дата операции": "2021-05-02", "Сумма операции": -345.50},
        ]
        savings = investment_bank("2021-05", transactions, 50)
        logger.info(f"Investment bank savings: {savings}")

        # Пример вызова spending_by_category (используем май 2021)
        transactions_df = read_transactions("data/operations.xlsx")
        category_report = spending_by_category(
            transactions_df, "Супермаркеты", "2021-05-20"
        )
        logger.info(f"Spending by category report: \n{category_report}")

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")


if __name__ == "__main__":
    main()
