import pytest
import pandas as pd
from src.views import homepage_view
from unittest.mock import patch


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return pd.DataFrame(
        {
            "Дата операции": [
                pd.to_datetime("2021-05-01 10:00:00"),
                pd.to_datetime("2021-05-02 12:00:00"),
            ],
            "Номер карты": ["1234", "5678"],
            "Сумма платежа": [-500.00, -300.00],
            "Категория": ["Супермаркеты", "Фастфуд"],
            "Описание": ["Лента", "KFC"],
            "Кэшбэк": [5.00, 3.00],
        }
    )


def test_homepage_view(sample_transactions):
    """Тест формирования JSON-ответа главной страницы"""
    with (
        patch("src.views.read_transactions") as mock_read_transactions,
        patch("src.views.get_currency_rates") as mock_currency_rates,
        patch("src.views.get_stock_prices") as mock_stock_prices,
    ):
        mock_read_transactions.return_value = sample_transactions
        mock_currency_rates.return_value = [{"currency": "USD", "rate": 75.0}]
        mock_stock_prices.return_value = [{"stock": "AAPL", "price": 150.0}]

        response = homepage_view("2021-05-20 14:30:00")
        assert response["greeting"] == "Добрый день"
        assert len(response["cards"]) == 2
        assert len(response["top_transactions"]) == 2
        assert response["currency_rates"] == [{"currency": "USD", "rate": 75.0}]
        assert response["stock_prices"] == [{"stock": "AAPL", "price": 150.0}]
