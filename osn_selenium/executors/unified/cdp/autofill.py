from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedAutofillCDPExecutor"]


class UnifiedAutofillCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Autofill.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Autofill.enable", {})
	
	def _set_addresses_impl(self, addresses: List[Dict[str, Any]]) -> None:
		return self._execute_function("Autofill.setAddresses", {"addresses": addresses})
	
	def _trigger_impl(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Dict[str, Any]] = None,
			address: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Autofill.trigger",
				{
					"field_id": field_id,
					"frame_id": frame_id,
					"card": card,
					"address": address
				}
		)
