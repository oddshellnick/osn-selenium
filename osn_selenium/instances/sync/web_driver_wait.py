from typing import (
	Callable,
	Self,
	TypeVar
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances._typehints import (
	WebDriverWaitInputType
)
from osn_selenium.instances.unified.web_driver_wait import UnifiedWebDriverWait
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)
from osn_selenium.abstract.instances.web_driver_wait import (
	AbstractWebDriverWait
)


__all__ = ["OUTPUT", "WebDriverWait"]

OUTPUT = TypeVar("OUTPUT")


class WebDriverWait(UnifiedWebDriverWait, AbstractWebDriverWait):
	"""
	Wrapper for the legacy Selenium WebDriverWait instance.

	Provides conditional waiting functionality, pausing execution until
	specific conditions (expected conditions) are met or a timeout occurs.
	"""
	
	def __init__(self, selenium_webdriver_wait: legacyWebDriverWait) -> None:
		"""
		Initializes the WebDriverWait wrapper.

		Args:
			selenium_webdriver_wait (legacyWebDriverWait): The legacy Selenium WebDriverWait instance to wrap.
		"""
		
		UnifiedWebDriverWait.__init__(self, selenium_webdriver_wait=selenium_webdriver_wait)
	
	@classmethod
	def from_legacy(cls, legacy_object: legacyWebDriverWait) -> Self:
		"""
		Creates a WebDriverWait wrapper instance from a legacy Selenium object.

		Args:
			legacy_object (legacyWebDriverWait): The legacy object to convert.

		Returns:
			Self: An instance of the WebDriverWait wrapper.

		Raises:
			CannotConvertTypeError: If the provided object cannot be converted to legacyWebDriverWait.
		"""
		
		legacy_wait_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_wait_obj, legacyWebDriverWait):
			raise CannotConvertTypeError(from_=legacyWebDriverWait, to_=legacy_object)
		
		return cls(selenium_webdriver_wait=legacy_wait_obj)
	
	@property
	def legacy(self) -> legacyWebDriverWait:
		return self._legacy_impl
	
	def until(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return self._until_impl(method=method, message=message)
	
	def until_not(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return self._until_not_impl(method=method, message=message)
