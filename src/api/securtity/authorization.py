__all__ = ["AuthorizationDependency"]

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .authentication import AuthCredentials


class Authorization:
    def __init__(self, credentials: AuthCredentials):
        self.auth_user_id = credentials.subject.get("id")
        self.auth_user_name = credentials.subject.get("username")
        self.auth_user_email = credentials.subject.get("email")
        self.auth_user_role = credentials.subject.get("role")

    @property
    def is_admin(self):
        return self.auth_user_role == "admin"

    @property
    def is_seller(self):
        role = self.auth_user_role
        return role == "admin" or role == "seller"

    @property
    def is_customer(self):
        role = self.auth_user_role
        return role == "admin" or role == "customer"

    @property
    def is_admin_or_raise(self):
        if self.auth_user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not have admin role",
            )

    @property
    def is_seller_or_raise(self):
        role = self.auth_user_role
        if role != "admin" and role != "seller":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not have seller role",
            )

    @property
    def is_customer_or_raise(self):
        role = self.auth_user_role
        if role != "admin" and role != "customer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not have customer role",
            )


AuthorizationDependency = Annotated[Authorization, Depends()]
