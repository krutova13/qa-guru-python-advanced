from typing import Generic, TypeVar, Type, Sequence

from sqlmodel import Session, select

from app.storage.base_storage import BaseStorage
from app.storage.database_engine import engine

T = TypeVar('T')
V = TypeVar('V')


class DatabaseStorage(BaseStorage[T], Generic[T]):
    def __init__(self, model_type: Type[T]):
        super().__init__(model_type)

    def save(self, obj: V) -> T:
        with Session(engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_all(self, page: int = 1, size: int = 10) -> Sequence[T]:
        with Session(engine) as session:
            stmt = select(self.model_type)
            return session.exec(stmt).all()

    def get_by_id(self, id: int) -> T | None:
        with Session(engine) as session:
            stmt = select(self.model_type).where(self.model_type.id == id)
            return session.exec(stmt).first()

    def update(self, id: int, obj: T) -> T | None:
        with Session(engine) as session:
            db_obj = session.get(self.model_type, id)
            data = obj.model_dump(exclude_unset=True)
            db_obj.sqlmodel_update(data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def delete(self, id: int) -> T | None:
        with Session(engine) as session:
            obj = session.get(self.model_type, id)
            if obj:
                session.delete(obj)
                session.commit()
            return obj
