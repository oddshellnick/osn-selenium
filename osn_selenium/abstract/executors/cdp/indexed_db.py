from abc import ABC, abstractmethod
from typing import (
	Any,
	List,
	Optional,
	Tuple
)


class AbstractIndexedDbCDPExecutor(ABC):
	@abstractmethod
	def clear_object_store(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> None:
		...
	
	@abstractmethod
	def delete_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None
	) -> None:
		...
	
	@abstractmethod
	def delete_object_store_entries(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None,
			key_range: Any = None
	) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_metadata(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> Tuple[float, float]:
		...
	
	@abstractmethod
	def request_data(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None,
			index_name: Optional[str] = None,
			skip_count: int = None,
			page_size: int = None,
			key_range: Optional[Any] = None
	) -> Tuple[List[Any], bool]:
		...
	
	@abstractmethod
	def request_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None
	) -> Any:
		...
	
	@abstractmethod
	def request_database_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None
	) -> List[str]:
		...
