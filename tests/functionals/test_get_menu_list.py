import http

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_menu_list(
    async_client: AsyncClient,
):
    response = await async_client.get(url="/api/v1/menus/")
    # print(response.json())
    print(response.status_code)
    # assert response.status_code == http.HTTPStatus.OK
    assert response.status_code == http.HTTPStatus.OK
    print(response.json())
