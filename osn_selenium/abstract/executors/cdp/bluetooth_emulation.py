from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractBluetoothEmulationCDPExecutor"]


class AbstractBluetoothEmulationCDPExecutor(ABC):
	@abstractmethod
	def add_characteristic(
			self,
			service_id: str,
			characteristic_uuid: str,
			properties: Dict[str, Any]
	) -> str:
		...
	
	@abstractmethod
	def add_descriptor(self, characteristic_id: str, descriptor_uuid: str) -> str:
		...
	
	@abstractmethod
	def add_service(self, address: str, service_uuid: str) -> str:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self, state: str, le_supported: bool) -> None:
		...
	
	@abstractmethod
	def remove_characteristic(self, characteristic_id: str) -> None:
		...
	
	@abstractmethod
	def remove_descriptor(self, descriptor_id: str) -> None:
		...
	
	@abstractmethod
	def remove_service(self, service_id: str) -> None:
		...
	
	@abstractmethod
	def set_simulated_central_state(self, state: str) -> None:
		...
	
	@abstractmethod
	def simulate_advertisement(self, entry: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def simulate_characteristic_operation_response(
			self,
			characteristic_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def simulate_descriptor_operation_response(
			self,
			descriptor_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def simulate_gatt_disconnection(self, address: str) -> None:
		...
	
	@abstractmethod
	def simulate_gatt_operation_response(self, address: str, type_: str, code: int) -> None:
		...
	
	@abstractmethod
	def simulate_preconnected_peripheral(
			self,
			address: str,
			name: str,
			manufacturer_data: List[Dict[str, Any]],
			known_service_uuids: List[str]
	) -> None:
		...
