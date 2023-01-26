import http
import uuid as uuid_pkg

from fastapi import APIRouter, Depends

from src.api.v1.services import SubmenuService, get_submenu_service
from src.models import (
    SubmenuCreate,
    SubmenuDetail,
    SubmenuList,
    SubmenuRead,
    SubmenuUpdate,
)
from src.schemas import StatusMessage

router = APIRouter(
    prefix="/menus/{menu_id}/submenus",
    tags=["submenus"],
)


@router.get(
    path="/",
    response_model=SubmenuList,
    summary="Список подменю",
    status_code=http.HTTPStatus.OK,
)
async def submenu_list(
    menu_id: uuid_pkg.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuList:
    return await submenu_service.get_list(menu_id=menu_id)


@router.get(
    path="/{submenu_id}",
    response_model=SubmenuDetail,
    summary="Конкретное подменю",
    status_code=http.HTTPStatus.OK,
)
async def submenu_detail(
    *,
    submenu_id: uuid_pkg.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuDetail:
    return await submenu_service.get_detail(submenu_id=submenu_id)


@router.post(
    path="/",
    response_model=SubmenuRead,
    summary="Создать подменю",
    status_code=http.HTTPStatus.CREATED,
)
async def submenu_create(
    menu_id: uuid_pkg.UUID,
    data: SubmenuCreate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuRead:
    return await submenu_service.create(menu_id=menu_id, data=data)


@router.patch(
    path="/{submenu_id}",
    response_model=SubmenuRead,
    summary="Обновить подменю",
    status_code=http.HTTPStatus.OK,
)
async def submenu_update(
    *,
    submenu_id: uuid_pkg.UUID,
    data: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuRead:
    return await submenu_service.update(submenu_id=submenu_id, data=data)


@router.delete(
    path="/{submenu_id}",
    response_model=StatusMessage,
    summary="Удалить подменю",
    status_code=http.HTTPStatus.OK,
)
async def submenu_delete(
    menu_id: uuid_pkg.UUID,
    submenu_id: uuid_pkg.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    is_deleted: bool = await submenu_service.delete(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    return StatusMessage(status=is_deleted, message="The submenu has been deleted")
