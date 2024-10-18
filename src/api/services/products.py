__all__ = ["ProductsServiceDependency", "ProductsService"]

from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId
from ..utils import validate_and_extract_data
from typing import List

from ..config import COLLECTIONS, db, logger
from ..models import Product, StoredProduct, UpdationProduct
from pydantic import ValidationError


class ProductsService:
    assert (collection_name := "products") in COLLECTIONS
    collection = db[collection_name]
    
    @classmethod
    def create_one(cls, product: Product):
        
        insertion_product = product.model_dump()  
        result = cls.collection.insert_one(insertion_product) 
        
        if result.inserted_id:
            insertion_product["_id"] = str(result.inserted_id)
            return insertion_product  
        else:
             raise Exception("Error al insertar el producto")

    @classmethod
    def get_all_active(cls) -> dict[str, list] :
        """Get all active products."""
     
        cursor = cls.collection.find({"deactivated_at":None})
        return validate_and_extract_data(cursor, StoredProduct)

    @classmethod
    def get_all_deleted(cls) -> List[StoredProduct]:
        """Get all deleted products."""
        cursor = cls.collection.find({"deactivated_at": {"$ne": None}})
        return validate_and_extract_data(cursor, StoredProduct)

    @classmethod
    def get_all(cls) -> List[StoredProduct]:
        """Get all products including deleted."""
        cursor = cls.collection.find()
        return validate_and_extract_data(cursor, StoredProduct)

    @classmethod
    def get_one(cls, id: PydanticObjectId):
        if db_product := cls.collection.find_one({"_id": id}):
            return StoredProduct.model_validate(db_product).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

    @classmethod
    def update_one(cls, id: PydanticObjectId, product: UpdationProduct):
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

    @classmethod
    def delete_one(cls, id: PydanticObjectId):
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
        

    @classmethod
    def delete_product_hard(cls, id: PydanticObjectId):
        document = cls.collection.find_one_and_delete({"_id": id})
        if document:
                validated_doc = StoredProduct.model_validate(document)
                return validated_doc.model_dump()
            


ProductsServiceDependency = Annotated[ProductsService, Depends()]
