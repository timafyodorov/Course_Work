import pandas as pd
from src.utils import read_transactions
from unittest.mock import patch


def test_read_transactions():
    """Тест для чтения транзакций из Excel"""
    with patch("pandas.read_excel") as mock_read_excel:
        mock_data = pd.DataFrame(
            {
                "Дата операции": ["01.05.2021 10:00:00"],
                "Номер карты": ["1234"],
                "Сумма платежа": [-500.00],
                "Категория": ["Супермаркеты"],
                "Описание": ["Лента"],
            }
        )
        mock_read_excel.return_value = mock_data
        df = read_transactions("data/operations.xlsx")
        assert not df.empty
        assert len(df) == 1
        assert df["Категория"].iloc[0] == "Супермаркеты"
