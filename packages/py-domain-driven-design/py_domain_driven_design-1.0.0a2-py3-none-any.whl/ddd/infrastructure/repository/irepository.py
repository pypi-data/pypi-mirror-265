from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: str) -> T:
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass
