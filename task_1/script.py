import logging
import sys

from pydantic import ValidationError

from logger_config import setup_logging
from task_1.csv_service import load_csv
from task_1.validate import UserValidateSchema

setup_logging()
log = logging.getLogger(__name__)


def print_table(users: list[UserValidateSchema]) -> None:
    if not users:
        log.info("Пользователи старше 18 лет не найдены")
        return

    print(f"{'Имя':<20} {'Email':<30} {'Возраст':<10}")
    print("-" * 60)

    for user in users:
        print(f"{user.name:<20} {str(user.email):<30} {user.age:>4}")


def main(file_path: str, delimiter: str = ",") -> None:
    log.info("Запуск обработки CSV-файла: %s", file_path)

    data = load_csv(file_path, delimiter)
    if not data:
        log.warning("Данные из CSV не получены")
        return

    result: list[UserValidateSchema] = []

    for item in data:
        try:
            user = UserValidateSchema(**item)
        except ValidationError:
            log.warning("Битый CSV-файл: ошибка валидации строки")
            return

        if user.age > 18:
            result.append(user)

    log.info("Количество пользователей старше 18 лет: %s", len(result))
    print_table(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        log.warning("Неверный запуск скрипта")
        print("Использование: poetry run python -m task_1.script <путь_к_файлу.csv>")
    else:
        main(sys.argv[1])