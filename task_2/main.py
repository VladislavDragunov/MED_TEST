import logging

import httpx

from logger_config import setup_logging
from task_2.app.services.fact_cat_service import FactCatService


setup_logging()
log = logging.getLogger(__name__)


async def main() -> None:
    log.info("Запуск task_2")

    async with httpx.AsyncClient() as client:
        service = FactCatService(client)
        fact = await service.get_fact()

        if fact is not None:
            service.save_fact(fact)
            log.info("Факт успешно сохранён")
        else:
            log.warning("Факт не был получен")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
