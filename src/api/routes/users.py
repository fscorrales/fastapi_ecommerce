from fastapi import APIRouter

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
def create_user():
    pass


@users_router.get("/")
def get_all_active_users():
    pass


@users_router.get("/deleted")
def get_all_deleted_users():
    pass


@users_router.get("/include_deleted")
def get_all_users():
    pass


@users_router.get("/me")
def get_me():
    pass


@users_router.get("/{id}")
def get_one_user():
    pass


@users_router.put("/{id}")
def update_user():
    pass


@users_router.delete("/{id}")
def delete_user():
    pass


@users_router.delete("/delete_forever/{id}")
def delete_user_forever():
    pass
