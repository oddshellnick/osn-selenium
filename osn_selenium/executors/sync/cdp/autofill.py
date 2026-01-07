from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.autofill import (
	AbstractAutofillCDPExecutor
)


class AutofillCDPExecutor(AbstractAutofillCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Autofill.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Autofill.enable", locals())
	
	def set_addresses(self, addresses: List[Any]) -> None:
		return self._execute_function("Autofill.setAddresses", locals())
	
	def trigger(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Any] = None,
			address: Optional[Any] = None
	) -> None:
		return self._execute_function("Autofill.trigger", locals())
