from typing import (
	Iterable,
	List,
	Optional
)
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium._typehints import DEVICES_TYPEHINT
from osn_selenium.webdrivers._bridges import (
	get_js_executor_bridge
)
from osn_selenium.instances.trio_threads.action_chains import ActionChains
from osn_selenium.webdrivers.trio_threads.core.script import CoreScriptMixin
from osn_selenium.instances.trio_threads.web_driver_wait import WebDriverWait
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.actions import (
	UnifiedCoreActionsMixin
)
from osn_selenium.abstract.webdriver.core.actions import (
	AbstractCoreActionsMixin
)


__all__ = ["CoreActionsMixin"]


class CoreActionsMixin(
		UnifiedCoreActionsMixin,
		CoreScriptMixin,
		TrioThreadMixin,
		AbstractCoreActionsMixin
):
	"""
	Mixin providing high-level interaction capabilities for Core WebDrivers.

	Includes factories for standard and human-like ActionChains, as well as
	custom WebDriverWait implementations.
	"""
	
	def action_chains(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> ActionChains:
		legacy = self._action_chains_impl(duration=duration, devices=devices)
		
		return ActionChains(
				selenium_action_chains=legacy,
				execute_js_script_function=get_js_executor_bridge(self),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	def web_driver_wait(
			self,
			timeout: float,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Iterable[BaseException]] = None,
	) -> WebDriverWait:
		legacy = self._web_driver_wait_impl(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions
		)
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=WebDriverWait,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
