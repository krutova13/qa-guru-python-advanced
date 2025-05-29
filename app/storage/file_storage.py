import json
from pathlib import Path
from typing import TypeVar, Generic, Type

from app.models.models import UserData, ProductData
from app.storage.base_storage import BaseStorage

T = TypeVar('T')


class FileStorage(BaseStorage[T], Generic[T]):

    def __init__(self, model_type: Type[T]):
        self.model_type = model_type
        self.file_path = self._get_file_path()
        self._ensure_file_exists()

    def _get_file_path(self) -> Path:
        if self.model_type == UserData:
            return Path("storage/users.json")
        elif self.model_type == ProductData:
            return Path("storage/products.json")
        else:
            return Path("storage/data.json")

    def _ensure_file_exists(self):
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            self.file_path.write_text("[]")

    def save(self, obj: T) -> T:
        data = self._read_data()
        obj_dict = obj.model_dump()
        data.append(obj_dict)
        self._write_data(data)
        return obj

    def get(self) -> list[T]:
        data = self._read_data()
        return [self.model_type.model_validate(item) for item in data]

    def get_by_id(self, id: str) -> T | None:
        data = self._read_data()
        for item in data:
            if item.get("id") == id:
                return self.model_type.model_validate(item)
        return None

    def delete(self, id: str) -> T | None:
        data = self._read_data()
        for i, item in enumerate(data):
            if item.get("id") == id:
                deleted_item = self.model_type.model_validate(item)
                del data[i]
                self._write_data(data)
                return deleted_item
        return None

    def _read_data(self) -> list[dict]:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _write_data(self, data: list[dict]):
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
