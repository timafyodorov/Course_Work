import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_transactions(file_path: str) -> pd.DataFrame:
    """Чтение данных транзакций из Excel-файла с указанными столбцами"""
    try:
        df = pd.read_excel(file_path)

        required_columns = [
            "Дата операции",
            "Номер карты",
            "Сумма платежа",
            "Категория",
            "Описание",
        ]
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            logger.error(f"Отсутствуют столбцы: {missing}")
            return pd.DataFrame()

        df["Дата операции"] = pd.to_datetime(
            df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
        )

        if df["Дата операции"].isna().any():
            logger.warning("Найдены строки с некорректными датами, они будут исключены")
            df = df.dropna(subset=["Дата операции"])

        logger.info("Данные транзакций успешно загружены")
        return df

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Ошибка при чтении файла: {e}")
        return pd.DataFrame()
