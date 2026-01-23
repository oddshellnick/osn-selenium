from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.autofill import (
	UnifiedAutofillCDPExecutor
)
from osn_selenium.abstract.executors.cdp.autofill import (
	AbstractAutofillCDPExecutor
)


__all__ = ["AutofillCDPExecutor"]


class AutofillCDPExecutor(UnifiedAutofillCDPExecutor, AbstractAutofillCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedAutofillCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def set_addresses(self, addresses: List[Dict[str, Any]]) -> None:
		return self._set_addresses_impl(addresses=addresses)
	
	def trigger(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Dict[str, Any]] = None,
			address: Optional[Dict[str, Any]] = None
	) -> None:
		return self._trigger_impl(field_id=field_id, frame_id=frame_id, card=card, address=address)
