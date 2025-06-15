from functools import wraps
from typing import Any

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import selectinload
from starlette import status

from app.exceptions.exceptions import NotFoundException


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except NotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return wrapper


def with_relations(*relations):
    def decorator(storage_class):
        class WrappedStorage(storage_class):
            def get_all(self, *args, **kwargs):
                stmt = super().get_all_query(*args, **kwargs)
                for relation in relations:
                    stmt = stmt.options(selectinload(getattr(self.model_type, relation)))
                return self._execute(stmt)

        return WrappedStorage

    return decorator
