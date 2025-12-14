from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.bluetoothemulation import (
	AbstractBluetoothEmulationCDPExecutor
)


class AsyncBluetoothEmulationCDPExecutor(AbstractBluetoothEmulationCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_characteristic(self, service_id: str, characteristic_uuid: str, properties: Any) -> str:
		return await self._execute_function("BluetoothEmulation.addCharacteristic", locals())
	
	async def add_descriptor(self, characteristic_id: str, descriptor_uuid: str) -> str:
		return await self._execute_function("BluetoothEmulation.addDescriptor", locals())
	
	async def add_service(self, address: str, service_uuid: str) -> str:
		return await self._execute_function("BluetoothEmulation.addService", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("BluetoothEmulation.disable", locals())
	
	async def enable(self, state: str, le_supported: bool) -> None:
		return await self._execute_function("BluetoothEmulation.enable", locals())
	
	async def remove_characteristic(self, characteristic_id: str) -> None:
		return await self._execute_function("BluetoothEmulation.removeCharacteristic", locals())
	
	async def remove_descriptor(self, descriptor_id: str) -> None:
		return await self._execute_function("BluetoothEmulation.removeDescriptor", locals())
	
	async def remove_service(self, service_id: str) -> None:
		return await self._execute_function("BluetoothEmulation.removeService", locals())
	
	async def set_simulated_central_state(self, state: str) -> None:
		return await self._execute_function("BluetoothEmulation.setSimulatedCentralState", locals())
	
	async def simulate_advertisement(self, entry: Any) -> None:
		return await self._execute_function("BluetoothEmulation.simulateAdvertisement", locals())
	
	async def simulate_characteristic_operation_response(
			self,
			characteristic_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return await self._execute_function("BluetoothEmulation.simulateCharacteristicOperationResponse", locals())
	
	async def simulate_descriptor_operation_response(
			self,
			descriptor_id: str,
			type_: str,
			code: int,
			data: Optional[str] = None
	) -> None:
		return await self._execute_function("BluetoothEmulation.simulateDescriptorOperationResponse", locals())
	
	async def simulate_gatt_disconnection(self, address: str) -> None:
		return await self._execute_function("BluetoothEmulation.simulateGATTDisconnection", locals())
	
	async def simulate_gatt_operation_response(self, address: str, type_: str, code: int) -> None:
		return await self._execute_function("BluetoothEmulation.simulateGATTOperationResponse", locals())
	
	async def simulate_preconnected_peripheral(
			self,
			address: str,
			name: str,
			manufacturer_data: List[Any],
			known_service_uuids: List[str]
	) -> None:
		return await self._execute_function("BluetoothEmulation.simulatePreconnectedPeripheral", locals())
