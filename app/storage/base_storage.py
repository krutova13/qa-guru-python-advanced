from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

T = TypeVar('T')


class BaseStorage(Generic[T], ABC):

    def __int__(self, model_type: Type[T]):
        self.model_type = model_type

    @abstractmethod
    def save(self, obj: T) -> T:
        pass

    @abstractmethod
    def get(self) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def delete(self, id: int) -> T | None:
        pass
