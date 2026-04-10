import logging
from typing import TYPE_CHECKING

from httpx import HTTPError

from task_2.app.core.config import settings

if TYPE_CHECKING:
    from httpx import AsyncClient


log = logging.getLogger(__name__)


class FactCatService:
    def __init__(self, client: "AsyncClient") -> None:
        self._client = client

    async def get_fact(self) -> str | None:
        try:
            log.info("Отправка запроса к API: %s", settings.host_by_str)

            response = await self._client.get(
                url=settings.host_by_str,
                timeout=settings.timeout,
            )
            response.raise_for_status()

            data = response.json()
            fact = data.get("fact")

            if fact:
                log.info("Факт успешно получен")
            else:
                log.warning("Ответ API получен, но факт отсутствует")

            return fact

        except HTTPError:
            log.warning("Не удалось получить факт")
            return None

    @staticmethod
    def save_fact(fact: str) -> None:
        settings.DATA_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(settings.DATA_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(fact)
            file.write("\n")

        log.info("Факт записан в файл: %s", settings.DATA_FILE_PATH)