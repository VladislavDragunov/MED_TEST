import csv
import logging

log = logging.getLogger(__name__)

def load_csv(file_path: str, delimiter: str = ",") -> list[dict] | None:
    if not file_path.endswith(".csv"):
        log.warning("Файл должен быть формата .csv")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = csv.DictReader(file, delimiter=delimiter)
            return list(data)

    except FileNotFoundError:
        log.warning("Файл не найден")
        return None
    except csv.Error:
        log.warning("Битый CSV-файл")
        return None