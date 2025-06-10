from typing import Iterable

from app.core.decorators import with_relations
from app.models.models import UserCreate, User
from app.storage.database.database_storage import DatabaseStorage


@with_relations("products")
class UserStorage(DatabaseStorage):

    def __init__(self):
        super().__init__(model_type=User)

    def save(self, user: UserCreate) -> User:
        return super().save(user)

    def get_all(self) -> Iterable[User]:
        return super().get_all()

    def get_by_id(self, user_id: int) -> User | None:
        return super().get_by_id(user_id)

    def update(self, user_id: int, user: User) -> User | None:
        return super().update(user_id, user)

    def delete(self, user_id: int) -> User | None:
        return super().delete(user_id)
