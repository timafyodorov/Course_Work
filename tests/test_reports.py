import pytest
import pandas as pd
from src.reports import spending_by_category
from datetime import datetime


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return pd.DataFrame(
        {
            "Дата операции": [
                datetime(2021, 5, 1),
                datetime(2021, 4, 15),
                datetime(2021, 3, 10),
            ],
            "Сумма платежа": [-500.00, -200.00, -150.00],
            "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"],
            "Описание": ["Лента", "Пятёрочка", "Метро"],
        }
    )


def test_spending_by_category(sample_transactions):
    """Тест отчёта по категории"""
    date_time_str = "2021-05-20"
    report = spending_by_category(sample_transactions, "Супермаркеты", date_time_str)
    assert not report.empty
    assert len(report) == 2
    assert all(report["Категория"] == "Супермаркеты")
    assert report["Сумма платежа"].sum() == -700.00
