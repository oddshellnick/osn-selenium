from typing import (
	Any,
	Callable,
	TypeVar
)
from osn_selenium.instances.errors import ExpectedTypeError
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.types import (
	WebDriverWaitInputType
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)


OUTPUT = TypeVar("OUTPUT")


class UnifiedWebDriverWait:
	def __init__(self, selenium_webdriver_wait: legacyWebDriverWait):
		if not isinstance(selenium_webdriver_wait, legacyWebDriverWait):
			raise ExpectedTypeError(
					expected_class=legacyWebDriverWait,
					received_instance=selenium_webdriver_wait
			)
		
		self._selenium_webdriver_wait = selenium_webdriver_wait
	
	def __repr__(self) -> str:
		return self._legacy_impl.__repr__()
	
	@property
	def _legacy_impl(self) -> legacyWebDriverWait:
		return self._selenium_webdriver_wait
	
	def __eq__(self, other: Any) -> bool:
		return self._legacy_impl == get_legacy_instance(instance=other)
	
	def __hash__(self) -> int:
		return self._legacy_impl.__hash__()
	
	def __ne__(self, other: Any) -> bool:
		return self._legacy_impl != get_legacy_instance(instance=other)
	
	def _until_impl(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return self._legacy_impl.until(method=method, message=message)
	
	def _until_not_impl(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return self._legacy_impl.until_not(method=method, message=message)
