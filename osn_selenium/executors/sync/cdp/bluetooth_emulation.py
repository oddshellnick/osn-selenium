from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.bluetooth_emulation import (
	UnifiedBluetoothEmulationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.bluetooth_emulation import (
	AbstractBluetoothEmulationCDPExecutor
)


__all__ = ["BluetoothEmulationCDPExecutor"]


class BluetoothEmulationCDPExecutor(
		UnifiedBluetoothEmulationCDPExecutor,
		AbstractBluetoothEmulationCDPExecutor
):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedBluetoothEmulationCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_characteristic(
			self,
			service_id: str,
			characteristic_uuid: str,
			properties: Dict[str, Any]
	) -> str:
		return self._add_characteristic_impl(
				service_id=service_id,
				characteristic_uuid=characteristic_uuid,
				properties=properties
		)
	
	def add_descriptor(self, characteristic_id: str, descriptor_uuid: str) -> str:
		return self._add_descriptor_impl(characteristic_id=characteristic_id, descriptor_uuid=descriptor_uuid)
	
	def add_service(self, address: str, service_uuid: str) -> str:
		return self._add_service_impl(address=address, service_uuid=service_uuid)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self, state: str, le_supported: bool) -> None:
		return self._enable_impl(state=state, le_supported=le_supported)
	
	def remove_characteristic(self, characteristic_id: str) -> None:
		return self._remove_characteristic_impl(characteristic_id=characteristic_id)
	
	def remove_descriptor(self, descriptor_id: str) -> None:
		return self._remove_descriptor_impl(descriptor_id=descriptor_id)
	
	def remove_service(self, service_id: str) -> None:
		return self._remove_service_impl(service_id=service_id)
	
	def set_simulated_central_state(self, state: str) -> None:
		return self._set_simulated_central_state_impl(state=state)
	
	def simulate_advertisement(self, entry: Dict[str, Any]) -> None:
		return self._simulate_advertisement_impl(entry=entry)
	
	def simulate_characteristic_operation_response(
			self,
			characteristic_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return self._simulate_characteristic_operation_response_impl(characteristic_id=characteristic_id, type_=type_, code=code, data=data)
	
	def simulate_descriptor_operation_response(
			self,
			descriptor_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return self._simulate_descriptor_operation_response_impl(descriptor_id=descriptor_id, type_=type_, code=code, data=data)
	
	def simulate_gatt_disconnection(self, address: str) -> None:
		return self._simulate_gatt_disconnection_impl(address=address)
	
	def simulate_gatt_operation_response(self, address: str, type_: str, code: int) -> None:
		return self._simulate_gatt_operation_response_impl(address=address, type_=type_, code=code)
	
	def simulate_preconnected_peripheral(
			self,
			address: str,
			name: str,
			manufacturer_data: List[Dict[str, Any]],
			known_service_uuids: List[str]
	) -> None:
		return self._simulate_preconnected_peripheral_impl(
				address=address,
				name=name,
				manufacturer_data=manufacturer_data,
				known_service_uuids=known_service_uuids
		)
