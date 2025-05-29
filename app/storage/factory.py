from typing import Type, TypeVar

from app.core.config import STORAGE_TYPE
from app.storage.base_storage import BaseStorage
from app.storage.file_storage import FileStorage

T = TypeVar('T')


class StorageFactory:
    _storages: dict[str, Type[BaseStorage]] = {
        "file": FileStorage
    }

    @classmethod
    def get_storage(cls, model_type: Type[T]) -> BaseStorage[T]:
        storage_class = cls._storages.get(STORAGE_TYPE)
        if not storage_class:
            raise ValueError(f"Тип хранилища {STORAGE_TYPE} не поддерживается")
        return storage_class(model_type=model_type)
