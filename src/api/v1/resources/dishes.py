import http
import uuid as uuid_pkg

from fastapi import APIRouter, Depends

from src.api.v1.services import DishService, get_dish_service
from src.models import DishCreate, DishList, DishRead, DishUpdate
from src.schemas import StatusMessage

router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dishes"],
)


@router.get(
    path="/",
    response_model=DishList,
    summary="Список блюд",
    status_code=http.HTTPStatus.OK,
)
async def dish_list(
    *,
    submenu_id: uuid_pkg.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> DishList:
    return await dish_service.get_list(submenu_id=submenu_id)


@router.get(
    path="/{dish_id}",
    response_model=DishRead,
    summary="Конкретное блюдо",
    status_code=http.HTTPStatus.OK,
)
async def dish_detail(
    *,
    dish_id: uuid_pkg.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> DishRead:
    return await dish_service.get_detail(dish_id=dish_id)


@router.post(
    path="/",
    response_model=DishRead,
    summary="Создать блюдо",
    status_code=http.HTTPStatus.CREATED,
)
async def dish_create(
    menu_id: uuid_pkg.UUID,
    submenu_id: uuid_pkg.UUID,
    data: DishCreate,
    dish_service: DishService = Depends(get_dish_service),
) -> DishRead:
    return await dish_service.create(menu_id=menu_id, submenu_id=submenu_id, data=data)


@router.patch(
    path="/{dish_id}",
    response_model=DishRead,
    summary="Обновить блюдо",
    status_code=http.HTTPStatus.OK,
)
async def dish_update(
    *,
    dish_id: uuid_pkg.UUID,
    data: DishUpdate,
    dish_service: DishService = Depends(get_dish_service),
) -> DishRead:
    return await dish_service.update(dish_id=dish_id, data=data)


@router.delete(
    path="/{dish_id}",
    response_model=StatusMessage,
    summary="Удалить блюдо",
    status_code=http.HTTPStatus.OK,
)
async def dish_delete(
    menu_id: uuid_pkg.UUID,
    submenu_id: uuid_pkg.UUID,
    dish_id: uuid_pkg.UUID,
    dish_service: DishService = Depends(get_dish_service),
):
    is_deleted: bool = await dish_service.delete(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
    return StatusMessage(status=is_deleted, message="The dish has been deleted")
