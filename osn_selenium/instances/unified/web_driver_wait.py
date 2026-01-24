from typing import Callable, TypeVar
from osn_selenium.exceptions.instance import NotExpectedTypeError
from osn_selenium.instances._typehints import (
	WebDriverWaitInputType
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)


__all__ = ["OUTPUT", "UnifiedWebDriverWait"]

OUTPUT = TypeVar("OUTPUT")


class UnifiedWebDriverWait:
	def __init__(self, selenium_webdriver_wait: legacyWebDriverWait):
		if not isinstance(selenium_webdriver_wait, legacyWebDriverWait):
			raise NotExpectedTypeError(
					expected_type=legacyWebDriverWait,
					received_instance=selenium_webdriver_wait
			)
		
		self._selenium_webdriver_wait = selenium_webdriver_wait
	
	def __repr__(self) -> str:
		return self._legacy_impl.__repr__()
	
	@property
	def _legacy_impl(self) -> legacyWebDriverWait:
		return self._selenium_webdriver_wait
	
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
