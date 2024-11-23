__all__ = ["serialize_object_id"]

from bson import ObjectId


def serialize_object_id(data):
    # Verifica si es un ObjectId y lo convierte a string
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, dict):
        return {k: serialize_object_id(v) for k, v in data.items()}
    if isinstance(data, list):
        return [serialize_object_id(item) for item in data]
    return data
