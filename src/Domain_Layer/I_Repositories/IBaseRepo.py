from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class IBaseRepo(ABC, Generic[T]):
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass

    @abstractmethod
    def _to_entity(self, orm) -> T:
        pass

    @abstractmethod
    def _to_orm(self, entity) -> T:
        pass