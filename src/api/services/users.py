__all__ = ["UsersService", "UsersServiceDependency"]

from ..config import db, COLLECTIONS

from fastapi import Depends
from typing import Annotated

from ..models import PublicStoredUser
from pydantic import ValidationError


class UsersService:
    assert (collection_name := "users") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def get_all(cls) -> dict[str, list]:
        """Get all users"""
        return_dict = {"response": [], "errors": []}
        users = cls.collection.find()
        for user in users:
            try:
                return_dict["response"].append(
                    PublicStoredUser.model_validate(user).model_dump()
                )
            except ValidationError as e:
                return_dict["errors"].append({"object": user, "details": str(e)})
        return return_dict

    @classmethod
    def get_all_deleted(cls) -> dict[str, list]:
        """Get all users"""
        return_dict = {"response": [], "errors": []}
        users = cls.collection.find({"deactivated_at": {"$ne": None}})
        for user in users:
            try:
                return_dict["response"].append(
                    PublicStoredUser.model_validate(user).model_dump()
                )
            except ValidationError as e:
                return_dict["errors"].append({"object": user, "details": str(e)})
        return return_dict

    @classmethod
    def get_all_active(cls) -> dict[str, list]:
        """Get all users"""
        return_dict = {"response": [], "errors": []}
        users = cls.collection.find({"deactivated_at": None})
        for user in users:
            try:
                return_dict["response"].append(
                    PublicStoredUser.model_validate(user).model_dump()
                )
            except ValidationError as e:
                return_dict["errors"].append({"object": user, "details": str(e)})
        return return_dict


UsersServiceDependency = Annotated[UsersService, Depends()]
