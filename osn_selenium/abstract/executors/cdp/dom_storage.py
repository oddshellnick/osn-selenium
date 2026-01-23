from typing import Any, Dict, List
from abc import ABC, abstractmethod


__all__ = ["AbstractDomStorageCDPExecutor"]


class AbstractDomStorageCDPExecutor(ABC):
	@abstractmethod
	def clear(self, storage_id: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_dom_storage_items(self, storage_id: Dict[str, Any]) -> List[List[str]]:
		...
	
	@abstractmethod
	def remove_dom_storage_item(self, storage_id: Dict[str, Any], key: str) -> None:
		...
	
	@abstractmethod
	def set_dom_storage_item(self, storage_id: Dict[str, Any], key: str, value: str) -> None:
		...
