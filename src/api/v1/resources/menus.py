import http
import uuid as uuid_pkg

from fastapi import APIRouter, Depends

from src.api.v1.schemas import StatusMessage
from src.models import MenuCreate, MenuRead, MenuDetail, MenuUpdate, MenuList
from src.api.v1.services import MenuService, get_menu_service

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['menus']
)


@router.get(
    path='/',
    response_model=MenuList,
    summary='Список меню',
    status_code=http.HTTPStatus.OK,
)
async def menu_list(
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuList:
    return await menu_service.get_list()


@router.get(
    path='/{menu_id}',
    response_model=MenuDetail,
    summary='Конкретное меню',
    status_code=http.HTTPStatus.OK,
)
async def menu_detail(
    menu_id: uuid_pkg.UUID,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuDetail:
    return await menu_service.get_detail(menu_id=menu_id)


@router.post(
    path='/',
    response_model=MenuRead,
    summary='Создать меню',
    status_code=http.HTTPStatus.CREATED,
)
async def menu_create(
    data: MenuCreate,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuRead:
    return await menu_service.create(data=data)


@router.patch(
    path='/{menu_id}',
    response_model=MenuRead,
    summary='Обновить меню',
    status_code=http.HTTPStatus.OK,
)
async def menu_update(
    menu_id: uuid_pkg.UUID,
    data: MenuUpdate,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuRead:
    return await menu_service.update(menu_id=menu_id, data=data)


@router.delete(
    path='/{menu_id}',
    response_model=StatusMessage,
    summary='Удалить меню',
    status_code=http.HTTPStatus.OK
)
async def menu_delete(
    menu_id: uuid_pkg.UUID,
    menu_service: MenuService = Depends(get_menu_service),
):
    is_deleted: bool = await menu_service.delete(menu_id=menu_id)
    return StatusMessage(status=is_deleted, message="The menu has been deleted")
