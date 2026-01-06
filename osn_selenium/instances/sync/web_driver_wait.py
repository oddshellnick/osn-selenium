from typing import (
	Callable,
	Self,
	TypeVar
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.types import (
	WebDriverWaitInputType
)
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)
from osn_selenium.abstract.instances.web_driver_wait import (
	AbstractWebDriverWait
)


OUTPUT = TypeVar("OUTPUT")


class WebDriverWait(AbstractWebDriverWait):
	def __init__(self, selenium_webdriver_wait: legacyWebDriverWait) -> None:
		if not isinstance(selenium_webdriver_wait, legacyWebDriverWait):
			raise ExpectedTypeError(
					expected_class=legacyWebDriverWait,
					received_instance=selenium_webdriver_wait
			)
		
		self._selenium_webdriver_wait = selenium_webdriver_wait
	
	@classmethod
	def from_legacy(cls, selenium_webdriver_wait: legacyWebDriverWait) -> Self:
		legacy_wait_obj = get_legacy_instance(selenium_webdriver_wait)
		
		if not isinstance(legacy_wait_obj, legacyWebDriverWait):
			raise TypesConvertError(from_=legacyWebDriverWait, to_=selenium_webdriver_wait)
		
		return cls(selenium_webdriver_wait=legacy_wait_obj)
	
	@property
	def legacy(self) -> legacyWebDriverWait:
		return self._selenium_webdriver_wait
	
	def until(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return self._selenium_webdriver_wait.until(method=method, message=message)
	
	def until_not(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return self._selenium_webdriver_wait.until_not(method=method, message=message)
