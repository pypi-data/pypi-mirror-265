from abc import ABC, abstractmethod
from google.cloud import datastore
from typing import Dict, List, TypeVar

from ddd.domain.model.exceptions.entity_not_found_exception import (
    EntityNotFoundException,
)
from ddd.infrastructure.repository.irepository import IRepository
from ddd.domain.model.entity import Entity

T = TypeVar("T", bound=Entity)


class DatastoreRepositoryBase(IRepository[T], ABC):
    def __init__(self, kind: str, client: datastore.Client = None):
        self.kind = kind
        self.client = client if client else datastore.Client()

    def get(self, id: str) -> T:
        key = self.client.key(self.kind, id)
        entity = self.client.get(key)
        return self._from_datastore(entity) if entity else None

    def save(self, entity: T) -> T:
        if not entity.id:
            raise AttributeError("The entity needs to have an ID.")
        key = self.client.key(self.kind, entity.id)
        datastore_entity = datastore.Entity(key=key)
        datastore_entity.update(self._to_datastore(entity))
        self.client.put(datastore_entity)
        return entity

    def find_all(self) -> List[T]:
        query = self.client.query(kind=self.kind)
        entities = list(query.fetch())
        return [self._from_datastore(entity) for entity in entities]

    def delete(self, id: str):
        key = self.client.key(self.kind, id)
        entity = self.client.get(key)
        if entity:
            self.client.delete(key)
        else:
            raise EntityNotFoundException(f"No entity found with ID: '{id}'")

    @abstractmethod
    def _from_datastore(self, entity: datastore.Entity) -> T:
        pass

    @abstractmethod
    def _to_datastore(self, entity: T) -> Dict:
        pass
