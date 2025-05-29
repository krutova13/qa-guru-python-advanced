from typing import Dict, Any

USER_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["id", "name", "surname", "birth_date", "products"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "surname": {"type": "string"},
        "birth_date": {
            "type": "string",
            "pattern": r"^\d{2}\.\d{2}\.\d{4}$"
        },
        "products": {
            "type": "array",
            "items": {"type": "object"}
        }
    }
}

USERS_LIST_SCHEMA: Dict[str, Any] = {
    "type": "array",
    "items": USER_SCHEMA
}

PRODUCT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["id", "title", "description", "price", "user_id"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "price": {"type": "number"},
        "user_id": {"type": "integer"}
    }
}

PRODUCTS_LIST_SCHEMA: Dict[str, Any] = {
    "type": "array",
    "items": PRODUCT_SCHEMA
}
