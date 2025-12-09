from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, List
from sqlalchemy.orm import Session
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from sqlalchemy.inspection import inspect


Entity = TypeVar("Entity")  # domain model
ORM = TypeVar("ORM") # sqlalchemy model

class BaseRepo(Generic[Entity], IBaseRepo[Entity]):

    def __init__(self, session: Session, model: Type[ORM]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Entity:

        orm = self.session.get(self.model, id)
        if orm is None:
            return None
        return self._to_entity(orm)

    def get_all(self) -> List[Entity]:
        orm_list = self.session.query(self.model).all() 
        return [self._to_entity(orm) for orm in orm_list]

    def add(self, entity ) -> Entity:
        orm = self._to_orm(entity)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._to_entity(orm)

    def update(self, updated_entity, id ) -> Entity:
        exist = self.session.get(self.model, id)
        if not exist:
            raise Exception(f"element with id = {id} doesn't exist")
        updated_orm = self._to_orm(updated_entity)
        mapper = inspect(updated_orm.__class__)
        pk_attr = mapper.primary_key[0].name
        setattr(updated_orm, pk_attr, id)
        merged = self.session.merge(updated_orm)
        self.session.commit()
        self.session.refresh(merged)
        return self._to_entity(merged)

    def delete(self, id: int) -> bool:
        obj = self.session.get(self.model, id)
        if obj is None:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
    
    @abstractmethod
    def _to_entity(self, orm):
        pass
    
    # @abstractmethod
    def _to_orm(self, entity):
        pass
