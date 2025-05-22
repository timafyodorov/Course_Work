from src.services import investment_bank


def test_investment_bank():
    """Тест расчёта инвест-копилки"""
    transactions = [
        {"Дата операции": "2021-05-01", "Сумма операции": -1712.00},
        {"Дата операции": "2021-05-02", "Сумма операции": -345.50},
    ]
    savings = investment_bank("2021-05", transactions, 50)
    assert savings == 42.5
