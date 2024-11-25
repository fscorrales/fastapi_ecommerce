from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from typing import Annotated

from ..services import UsersServiceDependency, AuthorizationDependency
from ..models import CreateUser, UpdateUser, FilterParamsUser, Role

from pydantic_mongo import PydanticObjectId

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/roles")
async def list_roles():
    roles_list = [item.value for item in Role]
    return roles_list


@users_router.post("/")
def create_user(
    user: CreateUser,
    users: UsersServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_raise()
        return users.create_one(user)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@users_router.get("/")
async def get_all_active_users(
    users: UsersServiceDependency, query: Annotated[FilterParamsUser, Query()]
):
    return users.get_all_active(query)


@users_router.get("/deleted")
async def get_all_deleted_users(
    users: UsersServiceDependency,
    security: AuthorizationDependency,
    query: Annotated[FilterParamsUser, Query()],
):
    security.is_admin_or_raise()
    return users.get_all_deleted(query)


@users_router.get("/include_deleted")
async def get_all_users(
    users: UsersServiceDependency,
    security: AuthorizationDependency,
    query: Annotated[FilterParamsUser, Query()],
):
    security.is_admin_or_raise()
    return users.get_all(query)


@users_router.get("/{id}")
async def get_one_user(id: PydanticObjectId, users: UsersServiceDependency):
    return users.get_one(id=id)


@users_router.put("/{id}")
async def update_user(
    id: PydanticObjectId,
    user: UpdateUser,
    users: UsersServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_same_user(id)
        return users.update_one(id=id, user=user, is_admin=security.is_admin)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@users_router.delete("/{id}")
async def delete_user(
    id: PydanticObjectId,
    users: UsersServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_same_user(id)
        return users.delete_one(id)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@users_router.delete("/delete_hard/{id}")
async def delete_user_hard(
    id: PydanticObjectId,
    users: UsersServiceDependency,
    security: AuthorizationDependency,
):
    try:
        security.is_admin_or_raise()
        return users.delete_one_hard(id)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
