from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.autofill import (
	AbstractAutofillCDPExecutor
)


class AutofillCDPExecutor(AbstractAutofillCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Autofill.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Autofill.enable", locals())
	
	async def set_addresses(self, addresses: List[List[Any]]) -> None:
		return await self._execute_function("Autofill.setAddresses", locals())
	
	async def trigger(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Any] = None,
			address: Optional[List[Any]] = None
	) -> None:
		return await self._execute_function("Autofill.trigger", locals())
