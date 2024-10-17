__all__ = ["validate_not_empty", "validate_and_extract_data"]

from pymongo.cursor import Cursor
from bson import ObjectId
from pydantic import BaseModel, ValidationError


def validate_not_empty(field: str) -> str:
    if not field:
        raise ValueError("field cannot be empty or zero")
    return field


def validate_and_extract_data(cursor: Cursor, model: BaseModel) -> dict[str, list]:
    """Validates and extracts data from MongoDB documents.

    Args:
        cursor (Cursor): MongoDB cursor.
        model (PydanticBaseModel): The model to use for validation.

    Returns:
        dict[str, list]: A dictionary with the validated and extracted data.
    """
    return_dict = {"response": [], "errors": []}
    for doc in cursor:
        try:
            validated_doc = model.model_validate(doc)
            return_dict["response"].append(validated_doc.model_dump())
        except ValidationError as e:
            doc_id = doc.get("_id")
            if isinstance(doc_id, ObjectId):
                doc["_id"] = str(doc_id)
            details = []
            for error in e.errors():
                details.append(
                    {
                        "loc": error["loc"],
                        "msg": error["msg"],
                        "type": error["type"],
                    }
                )
            return_dict["errors"].append({"doc_id": str(doc_id), "details": details})
    cursor.close()
    return return_dict
