__all__ = ["ProductsServiceDependency", "ProductsService"]

from datetime import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId
from ..utils import validate_and_extract_data
from ..config import COLLECTIONS, db, logger
from ..models import Product, StoredProduct, UpdationProduct
from pydantic import ValidationError


class ProductsService:
    assert (collection_name := "products") in COLLECTIONS
    collection = db[collection_name]
    
    @classmethod
    def create_one(cls, product: Product):
        try:
            insertion_product = product.model_dump()  
            result = cls.collection.insert_one(insertion_product) 
            
            if result.inserted_id:
                insertion_product["_id"] = str(result.inserted_id)
                return insertion_product  
            else:
                raise Exception("Error al insertar el producto")
        except Exception as e:
            logger.error(f"Error en create_one: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el producto")

    @classmethod
    def get_all_active(cls) -> dict[str, list]:
        """Get all active products."""
        try:
            cursor = cls.collection.find({"deactivated_at": None})
            return validate_and_extract_data(cursor, StoredProduct)
        except Exception as e:
            logger.error(f"Error en get_all_active: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener productos activos")

    @classmethod
    def get_all_deleted(cls) -> List[StoredProduct]:
        """Get all deleted products."""
        try:
            cursor = cls.collection.find({"deactivated_at": {"$ne": None}})
            return validate_and_extract_data(cursor, StoredProduct)
        except Exception as e:
            logger.error(f"Error en get_all_deleted: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener productos eliminados")

    @classmethod
    def get_all(cls) -> List[StoredProduct]:
        """Get all products including deleted."""
        try:
            cursor = cls.collection.find()
            return validate_and_extract_data(cursor, StoredProduct)
        except Exception as e:
            logger.error(f"Error en get_all: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener todos los productos")

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
            logger.error(f"Error en get_one: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener el producto")

    @classmethod
    def update_one(cls, id: PydanticObjectId, product: UpdationProduct):
        try:
            product_dict = product.model_dump(exclude_unset=True)
            document = cls.collection.find_one_and_update(
                {"_id": id},
                {"$set": product_dict},
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
            logger.error(f"Error en update_one: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el producto")

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
            logger.error(f"Error en delete_one: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el producto")

    @classmethod
    def delete_product_hard(cls, id: PydanticObjectId):
        try:
            document = cls.collection.find_one_and_delete({"_id": id})
            if document:
                validated_doc = StoredProduct.model_validate(document)
                return validated_doc.model_dump()
        except Exception as e:
            logger.error(f"Error en delete_product_hard: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el producto de forma permanente")

    @classmethod
    def get_by_seller(cls, seller_id: PydanticObjectId):
        try:
            cursor = cls.collection.find({"seller_id": seller_id})
            products = list(cursor)
            if products:
                return [StoredProduct.model_validate(product).model_dump() for product in products]
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No products found for the seller"
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en get_by_seller: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener productos por vendedor")


ProductsServiceDependency = Annotated[ProductsService, Depends()]
