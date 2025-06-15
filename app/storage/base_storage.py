from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Iterable

T = TypeVar('T')


class BaseStorage(Generic[T], ABC):
    def __init__(self, model_type: Type[T]):
        self.model_type = model_type

    @abstractmethod
    def save(self, obj: T) -> T:
        pass

    @abstractmethod
    def get_all(self, page: int = 1, size: int = 10) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def update(self, id: int, obj: T) -> T | None:
        pass

    @abstractmethod
    def delete(self, id: int) -> T | None:
        pass
