import logging
from pandas import to_datetime, DataFrame
from datetime import datetime, timedelta
from typing import Optional, Callable
from functools import wraps
import json

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def save_report(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата отчета в файл"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_file = (
                filename
                if filename
                else f"{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(
                        result.to_dict(orient="records"),
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )
                logger.info(f"Отчет сохранен в файл {output_file}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")
            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(
    transactions: DataFrame, category: str, date: Optional[str] = None
) -> DataFrame:
    """Анализ трат по заданной категории за последние три месяца"""
    try:
        if date:
            end_date = to_datetime(date, format="%Y-%m-%d")
        else:
            end_date = datetime.now()

        start_date = end_date - timedelta(days=90)

        transactions["Дата операции"] = to_datetime(
            transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
        )
        mask = (
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
            & (transactions["Сумма платежа"] < 0)
        )
        filtered_transactions = transactions[mask][
            ["Дата операции", "Сумма платежа", "Категория", "Описание"]
        ].copy()

        filtered_transactions["Дата операции"] = filtered_transactions[
            "Дата операции"
        ].dt.strftime("%Y-%m-%d")
        filtered_transactions["Сумма платежа"] = filtered_transactions[
            "Сумма платежа"
        ].abs()

        logger.info(f"Отчет по категории '{category}' успешно сформирован")
        return filtered_transactions

    except ValueError as e:
        logger.error(f"Ошибка формата даты: {e}")
        return DataFrame()
    except Exception as e:
        logger.error(f"Ошибка при формировании отчета: {e}")
        return DataFrame()
