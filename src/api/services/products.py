__all__ = ["ProductsServiceDependency", "ProductsService"]

from datetime import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId
from ..utils import validate_and_extract_data
from ..config import COLLECTIONS, db, logger
from ..models import CreateProduct, StoredProduct, UpdateProduct
from pydantic import ValidationError


class ProductsService:
    assert (collection_name := "products") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def create_one(cls, product: CreateProduct):
        try:
            insertion_product = product.model_dump(exclude_unset=False)
            new_product = cls.collection.insert_one(insertion_product)
            return StoredProduct.model_validate(
                cls.collection.find_one(new_product.inserted_id)
            )
        except Exception as e:
            logger.error(f"Error in create_one: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating product",
            )

    @classmethod
    def get_all_active(cls) -> dict[str, list]:
        """Get all active products."""
        try:
            cursor = cls.collection.find({"deactivated_at": None})
            return validate_and_extract_data(cursor, StoredProduct)
        except Exception as e:
            logger.error(f"Error in get_all_active: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting active products",
            )

    @classmethod
    def get_all_deleted(cls) -> List[StoredProduct]:
        """Get all deleted products."""
        try:
            cursor = cls.collection.find({"deactivated_at": {"$ne": None}})
            return validate_and_extract_data(cursor, StoredProduct)
        except Exception as e:
            logger.error(f"Error in get_all_deleted: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting deleted products",
            )

    @classmethod
    def get_all(cls) -> List[StoredProduct]:
        """Get all products including deleted."""
        try:
            cursor = cls.collection.find()
            return validate_and_extract_data(cursor, StoredProduct)
        except Exception as e:
            logger.error(f"Error in get_all: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting all products",
            )

    @classmethod
    def get_one(cls, id: PydanticObjectId):
        try:
            if db_product := cls.collection.find_one({"_id": id}):
                return StoredProduct.model_validate(db_product).model_dump()
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_one: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting one product",
            )

    @classmethod
    def update_one(cls, id: PydanticObjectId, product: UpdateProduct):
        document = cls.collection.find_one_and_update(
            {"_id": id},
            {"$set": product.model_dump(exclude_unset=True)},
            return_document=True,
        )
        if document:
            try:
                return StoredProduct.model_validate(document).model_dump()
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT, detail=str(e)
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

    @classmethod
    def delete_one(cls, id: PydanticObjectId):
        try:
            document = cls.collection.find_one_and_update(
                {"_id": id},
                {"$set": {"deactivated_at": datetime.now()}},
                return_document=True,
            )
            if document:
                return StoredProduct.model_validate(document).model_dump()
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error einn delete_one: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting one product",
            )

    @classmethod
    def delete_one_hard(cls, id: PydanticObjectId):
        try:
            document = cls.collection.find_one_and_delete({"_id": id})
            if document:
                validated_doc = StoredProduct.model_validate(document)
                return validated_doc.model_dump()
        except Exception as e:
            logger.error(f"Error in delete_product_hard: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error permanently deleting the product",
            )

    @classmethod
    def get_by_seller(cls, seller_id: PydanticObjectId):
        try:
            cursor = cls.collection.find({"seller_id": seller_id})
            products = list(cursor)
            if products:
                return [
                    StoredProduct.model_validate(product).model_dump()
                    for product in products
                ]
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No products found for the seller",
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_by_seller: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting products by seller",
            )


ProductsServiceDependency = Annotated[ProductsService, Depends()]
