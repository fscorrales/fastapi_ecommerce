__all__ = ["UsersService", "UsersServiceDependency"]

from ..config import db, COLLECTIONS
from ..utils import validate_and_extract_data

from fastapi import Depends, HTTPException, status
from typing import Annotated

from ..models import PublicStoredUser, PrivateStoredUser, CreateUser
from pydantic import ValidationError
from pydantic_mongo import PydanticObjectId
from bson import ObjectId


class UsersService:
    assert (collection_name := "users") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def create_one(cls, user: CreateUser) -> PublicStoredUser:
        """Create a new user"""
        existing_user = cls.collection.find_one(
            {
                "$or": [
                    {"username": user.username},
                    {"email": user.email},
                ]
            }
        )
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

        insert_user = user.model_dump(exclude={"password"}, exclude_unset=False)
        insert_user.update(hash_password="not_hashed_yet")

        new_user = cls.collection.insert_one(insert_user)
        return PublicStoredUser.model_validate(
            cls.collection.find_one(new_user.inserted_id)
        )

    @classmethod
    def get_one(
        cls,
        *,
        id: PydanticObjectId | None = None,
        username: str | None = None,
        email: str | None = None,
        with_password: bool = False,
    ):
        if all(q is None for q in (id, username, email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No id, username or email provided",
            )
        filter = {
            "$or": [
                {"_id": id},
                {"username": username},
                {"email": email},
            ]
        }

        if db_user := cls.collection.find_one(filter):
            return (
                PrivateStoredUser.model_validate(db_user).model_dump()
                if with_password
                else PublicStoredUser.model_validate(db_user).model_dump()
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    @classmethod
    def get_all(cls) -> dict[str, list]:
        """Get all users"""
        return_dict = {"response": [], "errors": []}
        cursor = cls.collection.find()
        return validate_and_extract_data(cursor, PublicStoredUser)

    @classmethod
    def get_all_deleted(cls) -> dict[str, list]:
        """Get all users"""
        return_dict = {"response": [], "errors": []}
        cursor = cls.collection.find({"deactivated_at": {"$ne": None}})
        return validate_and_extract_data(cursor, PublicStoredUser)

    @classmethod
    def get_all_active(cls) -> dict[str, list]:
        """Get all active users"""
        cursor = cls.collection.find({"deactivated_at": None})
        return validate_and_extract_data(cursor, PublicStoredUser)


UsersServiceDependency = Annotated[UsersService, Depends()]
