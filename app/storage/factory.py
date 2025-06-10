import os
from typing import Type, TypeVar

from app.storage.base_storage import BaseStorage
from app.storage.database.database_storage import DatabaseStorage
from app.storage.file_storage import FileStorage

T = TypeVar('T')


class StorageFactory:
    _storages: dict[str, Type[BaseStorage]] = {
        "file": FileStorage,
        "database": DatabaseStorage
    }

    @classmethod
    def get_storage(cls, model_type: Type[T]) -> BaseStorage[T]:
        storage: str = os.getenv("STORAGE_TYPE")
        storage_class = cls._storages.get(storage)
        if not storage_class:
            raise ValueError(f"Тип хранилища {storage} не поддерживается")
        return storage_class(model_type=model_type)
