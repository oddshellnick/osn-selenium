from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.bluetooth_emulation import (
	AbstractBluetoothEmulationCDPExecutor
)


class BluetoothEmulationCDPExecutor(AbstractBluetoothEmulationCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def add_characteristic(self, service_id: str, characteristic_uuid: str, properties: Any) -> str:
		return self._execute_function("BluetoothEmulation.addCharacteristic", locals())
	
	def add_descriptor(self, characteristic_id: str, descriptor_uuid: str) -> str:
		return self._execute_function("BluetoothEmulation.addDescriptor", locals())
	
	def add_service(self, address: str, service_uuid: str) -> str:
		return self._execute_function("BluetoothEmulation.addService", locals())
	
	def disable(self) -> None:
		return self._execute_function("BluetoothEmulation.disable", locals())
	
	def enable(self, state: str, le_supported: bool) -> None:
		return self._execute_function("BluetoothEmulation.enable", locals())
	
	def remove_characteristic(self, characteristic_id: str) -> None:
		return self._execute_function("BluetoothEmulation.removeCharacteristic", locals())
	
	def remove_descriptor(self, descriptor_id: str) -> None:
		return self._execute_function("BluetoothEmulation.removeDescriptor", locals())
	
	def remove_service(self, service_id: str) -> None:
		return self._execute_function("BluetoothEmulation.removeService", locals())
	
	def set_simulated_central_state(self, state: str) -> None:
		return self._execute_function("BluetoothEmulation.setSimulatedCentralState", locals())
	
	def simulate_advertisement(self, entry: Any) -> None:
		return self._execute_function("BluetoothEmulation.simulateAdvertisement", locals())
	
	def simulate_characteristic_operation_response(
			self,
			characteristic_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return self._execute_function("BluetoothEmulation.simulateCharacteristicOperationResponse", locals())
	
	def simulate_descriptor_operation_response(
			self,
			descriptor_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return self._execute_function("BluetoothEmulation.simulateDescriptorOperationResponse", locals())
	
	def simulate_gatt_disconnection(self, address: str) -> None:
		return self._execute_function("BluetoothEmulation.simulateGATTDisconnection", locals())
	
	def simulate_gatt_operation_response(self, address: str, type_: str, code: int) -> None:
		return self._execute_function("BluetoothEmulation.simulateGATTOperationResponse", locals())
	
	def simulate_preconnected_peripheral(
			self,
			address: str,
			name: str,
			manufacturer_data: List[Any],
			known_service_uuids: List[str]
	) -> None:
		return self._execute_function("BluetoothEmulation.simulatePreconnectedPeripheral", locals())
