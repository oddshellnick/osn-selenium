from typing import Any, Callable
from osn_selenium.instances.errors import ExpectedTypeError
from osn_selenium.executors.unified.javascript import UnifiedJSExecutor
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


class UnifiedBaseMixin:
	def __init__(
			self,
			selenium_action_chains: legacyActionChains,
			execute_js_script_function: Callable[[str, Any], Any]
	):
		if not isinstance(selenium_action_chains, legacyActionChains):
			raise ExpectedTypeError(
					expected_class=legacyActionChains,
					received_instance=selenium_action_chains
			)
		
		self._selenium_action_chains = selenium_action_chains
		self._execute_js_script_function = execute_js_script_function
		
		self._js_executor = UnifiedJSExecutor(execute_function=execute_js_script_function)
	
	@property
	def _legacy_impl(self) -> legacyActionChains:
		return self._selenium_action_chains
