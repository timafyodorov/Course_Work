from src.services import get_currency_rates, get_stock_prices
from unittest.mock import patch


def test_get_currency_rates():
    """Тест получения курсов валют"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"USD": 75.0, "EUR": 85.0}}
        rates = get_currency_rates()
        assert len(rates) == 2
        assert rates[0]["currency"] in ["USD", "EUR"]
        assert isinstance(rates[0]["rate"], float)


def test_get_stock_prices():
    """Тест получения цен акций"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Global Quote": {"05. price": "150.00"}
        }
        prices = get_stock_prices()
        assert len(prices) <= 5
        if prices:
            assert prices[0]["stock"] in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
            assert isinstance(prices[0]["price"], float)
