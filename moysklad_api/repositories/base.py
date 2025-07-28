"""
Base repository for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Union, Tuple, TypeVar, Generic, Type
from dataclasses import asdict

from ..api_client import ApiClient
from ..query import QueryBuilder
from ..entities.base import MetaEntity, Meta, ListEntity


T = TypeVar('T', bound=MetaEntity)


class EntityRepository(Generic[T]):
    """Base repository for MoySklad entities."""

    def __init__(self, api_client: ApiClient, entity_name: str, entity_class: Type[T]):
        """
        Initialize entity repository.

        Args:
            api_client: API client instance
            entity_name: Entity API endpoint name
            entity_class: Entity class
        """
        self.api_client = api_client
        self.entity_name = entity_name
        self.entity_class = entity_class

    def find_all(self, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[T], Meta]:
        """
        Find all entities matching the query.

        Args:
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of entities, metadata)
        """
        params = query_builder.to_params() if query_builder else {}
        response = self.api_client.get(self.entity_name, params=params)

        data = ListEntity.from_dict(response, self.entity_class)

        return data.rows, data.meta
    
    def fetch_all(self, query_builder: Optional[QueryBuilder] = None) -> List[T]:
        """
        Fetches all entities matching the query from all pages.
        
        Args:
            query_builder: Query builer for filtering, sorting, etc.
        Returns:
            List of entities.
        """
        params = query_builder.to_params() if query_builder else {}
        response = self.api_client.get(self.entity_name, params=params)
        data = ListEntity.from_dict(response, self.entity_class)

        list_entities: List[T]  = data.rows

        while (data.meta.nextHref):
            response = self.api_client.get_via_url(data.meta.nextHref)
            data = ListEntity.from_dict(response, self.entity_class)

            if len(data.rows) > 0:
                list_entities.append(data.rows)
            
        return list_entities


    def find_by_id(self, entity_id: str, query_builder: Optional[QueryBuilder] = None) -> T:
        """
        Find an entity by ID.

        Args:
            entity_id: Entity ID
            query_builder: Query builder for expanding related entities
            expand: Expand related fields

        Returns:
            Entity instance

        Raises:
            NotFoundException: When entity is not found
        """
        params = query_builder.to_params() if query_builder else {}
        response = self.api_client.get(f"{self.entity_name}/{entity_id}", params=params)
        return self.entity_class.from_dict(response)

    def create(self, entity: T) -> T:
        """
        Create a new entity.

        Args:
            entity: Entity instance to create

        Returns:
            Created entity instance with ID

        Raises:
            ValidationException: When entity validation fails
        """
        data = entity.to_dict()
        response = self.api_client.post(self.entity_name, data=data)
        return self.entity_class.from_dict(response)

    def update(self, entity: T) -> T:
        """
        Update an existing entity.

        Args:
            entity: Entity instance to update

        Returns:
            Updated entity instance

        Raises:
            NotFoundException: When entity is not found
            ValidationException: When entity validation fails
        """
        if not entity.id:
            raise ValueError("Entity must have an ID for update operation")

        data = entity.to_dict()
        response = self.api_client.put(f"{self.entity_name}/{entity.id}", data=data)
        return self.entity_class.from_dict(response)

    def delete(self, entity_id: str) -> None:
        """
        Delete an entity by ID.

        Args:
            entity_id: Entity ID

        Raises:
            NotFoundException: When entity is not found
        """
        self.api_client.delete(f"{self.entity_name}/{entity_id}")

    def metadata(self) -> Dict:
        """
        Get entity metadata.

        Returns:
            Metadata dictionary
        """
        return self.api_client.get(f"{self.entity_name}/metadata")

    def query(self) -> QueryBuilder:
        """
        Create a new query builder for this entity.

        Returns:
            Query builder instance
        """
        return QueryBuilder()

    def create_bulk(self, entities: List[T]) -> List[T]:
        """
        Create multiple entities in a single request.

        Args:
            entities: List of entity instances to create

        Returns:
            List of created entity instances with IDs

        Raises:
            ValidationException: When entity validation fails
        """
        data = [entity.to_dict() for entity in entities]
        response = self.api_client.post(self.entity_name, data=data)

        if "rows" in response:
            return [self.entity_class.from_dict(row) for row in response.get("rows", [])]
        return [self.entity_class.from_dict(response)]

    def update_bulk(self, entities: List[T]) -> List[T]:
        """
        Update multiple entities in a single request.

        Args:
            entities: List of entity instances to update

        Returns:
            List of updated entity instances

        Raises:
            ValidationException: When entity validation fails
        """
        for entity in entities:
            if not entity.id:
                raise ValueError("All entities must have an ID for bulk update operation")

        data = [entity.to_dict() for entity in entities]
        response = self.api_client.post(self.entity_name, data=data)

        if "rows" in response:
            return [self.entity_class.from_dict(row) for row in response.get("rows", [])]
        return [self.entity_class.from_dict(response)]

    def delete_bulk(self, entity_ids: List[str]) -> None:
        """
        Delete multiple entities in a single request.

        Args:
            entity_ids: List of entity IDs to delete
        """
        self.api_client.post(f"{self.entity_name}/delete", data=entity_ids)