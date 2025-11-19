from typing import (
	Any,
	Callable,
	TYPE_CHECKING,
	cast
)
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from osn_selenium.abstract.instances.action_chains.base import AbstractBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["BaseMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class BaseMixin(UnifiedBaseMixin, AbstractBaseMixin):
	"""
	Base mixin class that bridges legacy Selenium actions with unified execution logic.
	"""
	
	def __init__(
			self,
			selenium_action_chains: legacyActionChains,
			execute_js_script_function: Callable[[str, Any], Any]
	):
		"""
		Initializes an ActionChains instance from a legacy Selenium ActionChains object.

		Args:
			selenium_action_chains (legacyActionChains): The legacy Selenium action chain.
			execute_js_script_function (Callable[[str, Any], Any]): The function used to execute JS.

		Returns:
			"ActionChains": The ActionChains instance.
		"""
		
		UnifiedBaseMixin.__init__(
				self,
				selenium_action_chains=selenium_action_chains,
				execute_js_script_function=execute_js_script_function,
		)
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: legacyActionChains,
			execute_js_script_function: Callable[[str, Any], Any],
	) -> "ActionChains":
		"""
		Creates an ActionChains instance from a legacy Selenium ActionChains object.

		Args:
			legacy_object (legacyActionChains): The legacy Selenium action chain.
			execute_js_script_function (Callable[[str, Any], Any]): The function used to execute JS.

		Returns:
			"ActionChains": The ActionChains instance.
		"""
		
		return cast(
				"ActionChains",
				cls(
						selenium_action_chains=legacy_object,
						execute_js_script_function=execute_js_script_function,
				)
		)
	
	@property
	def legacy(self) -> legacyActionChains:
		return self._legacy_impl
