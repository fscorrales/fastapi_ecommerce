from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..services import UsersServiceDependency
from ..models import CreateUser

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def create_user(user: CreateUser, users: UsersServiceDependency):
    try:
        created_user = users.create_one(user)
        return created_user
    except HTTPException as e:
        # Manejar la excepción y devolver una respuesta de error
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@users_router.get("/")
async def get_all_active_users(users: UsersServiceDependency):
    return users.get_all_active()


@users_router.get("/deleted")
async def get_all_deleted_users(users: UsersServiceDependency):
    return users.get_all_deleted()


@users_router.get("/include_deleted")
async def get_all_users(users: UsersServiceDependency):
    return users.get_all()


@users_router.get("/me")
async def get_me():
    pass


@users_router.get("/{id}")
async def get_one_user():
    pass


@users_router.put("/{id}")
async def update_user():
    pass


@users_router.delete("/{id}")
async def delete_user():
    pass


@users_router.delete("/delete_forever/{id}")
async def delete_user_forever():
    pass
