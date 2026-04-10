import logging
import sys
from pathlib import Path

import httpx
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from task_2.app.services.fact_cat_service import FactCatService


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [400, 500])
async def test_get_fact_returns_none_on_http_error(
    status_code: int,
    caplog: pytest.LogCaptureFixture,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=status_code,
            json={"detail": "error"},
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with caplog.at_level(logging.WARNING):
        async with httpx.AsyncClient(transport=transport) as client:
            service = FactCatService(client)
            fact = await service.get_fact()

    assert fact is None
    assert "Не удалось получить факт" in caplog.text