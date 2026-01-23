from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedBluetoothEmulationCDPExecutor"]


class UnifiedBluetoothEmulationCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_characteristic_impl(
			self,
			service_id: str,
			characteristic_uuid: str,
			properties: Dict[str, Any]
	) -> str:
		return self._execute_function(
				"BluetoothEmulation.addCharacteristic",
				{
					"service_id": service_id,
					"characteristic_uuid": characteristic_uuid,
					"properties": properties
				}
		)
	
	def _add_descriptor_impl(self, characteristic_id: str, descriptor_uuid: str) -> str:
		return self._execute_function(
				"BluetoothEmulation.addDescriptor",
				{
					"characteristic_id": characteristic_id,
					"descriptor_uuid": descriptor_uuid
				}
		)
	
	def _add_service_impl(self, address: str, service_uuid: str) -> str:
		return self._execute_function(
				"BluetoothEmulation.addService",
				{"address": address, "service_uuid": service_uuid}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("BluetoothEmulation.disable", {})
	
	def _enable_impl(self, state: str, le_supported: bool) -> None:
		return self._execute_function(
				"BluetoothEmulation.enable",
				{"state": state, "le_supported": le_supported}
		)
	
	def _remove_characteristic_impl(self, characteristic_id: str) -> None:
		return self._execute_function(
				"BluetoothEmulation.removeCharacteristic",
				{"characteristic_id": characteristic_id}
		)
	
	def _remove_descriptor_impl(self, descriptor_id: str) -> None:
		return self._execute_function("BluetoothEmulation.removeDescriptor", {"descriptor_id": descriptor_id})
	
	def _remove_service_impl(self, service_id: str) -> None:
		return self._execute_function("BluetoothEmulation.removeService", {"service_id": service_id})
	
	def _set_simulated_central_state_impl(self, state: str) -> None:
		return self._execute_function("BluetoothEmulation.setSimulatedCentralState", {"state": state})
	
	def _simulate_advertisement_impl(self, entry: Dict[str, Any]) -> None:
		return self._execute_function("BluetoothEmulation.simulateAdvertisement", {"entry": entry})
	
	def _simulate_characteristic_operation_response_impl(
			self,
			characteristic_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return self._execute_function(
				"BluetoothEmulation.simulateCharacteristicOperationResponse",
				{
					"characteristic_id": characteristic_id,
					"type_": type_,
					"code": code,
					"data": data
				}
		)
	
	def _simulate_descriptor_operation_response_impl(
			self,
			descriptor_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return self._execute_function(
				"BluetoothEmulation.simulateDescriptorOperationResponse",
				{
					"descriptor_id": descriptor_id,
					"type_": type_,
					"code": code,
					"data": data
				}
		)
	
	def _simulate_gatt_disconnection_impl(self, address: str) -> None:
		return self._execute_function("BluetoothEmulation.simulateGATTDisconnection", {"address": address})
	
	def _simulate_gatt_operation_response_impl(self, address: str, type_: str, code: int) -> None:
		return self._execute_function(
				"BluetoothEmulation.simulateGATTOperationResponse",
				{"address": address, "type_": type_, "code": code}
		)
	
	def _simulate_preconnected_peripheral_impl(
			self,
			address: str,
			name: str,
			manufacturer_data: List[Dict[str, Any]],
			known_service_uuids: List[str]
	) -> None:
		return self._execute_function(
				"BluetoothEmulation.simulatePreconnectedPeripheral",
				{
					"address": address,
					"name": name,
					"manufacturer_data": manufacturer_data,
					"known_service_uuids": known_service_uuids
				}
		)
