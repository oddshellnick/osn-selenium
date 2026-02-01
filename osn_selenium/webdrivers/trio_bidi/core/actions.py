from typing_extensions import deprecated
from typing import (
	Iterable,
	List,
	Optional
)
from osn_selenium._typehints import DEVICES_TYPEHINT
from osn_selenium.trio_bidi.mixin import TrioBiDiMixin
from osn_selenium.webdrivers.trio_bidi.core.script import CoreScriptMixin
from osn_selenium.instances.trio_bidi.web_driver_wait import WebDriverWait
from osn_selenium.instances.convert import (
	get_trio_bidi_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.actions import (
	UnifiedCoreActionsMixin
)
from osn_selenium.abstract.webdriver.core.actions import (
	AbstractCoreActionsMixin
)
from osn_selenium.exceptions.experimental import (
	NotImplementedExperimentalFeatureError
)


__all__ = ["CoreActionsMixin"]


class CoreActionsMixin(
		UnifiedCoreActionsMixin,
		CoreScriptMixin,
		TrioBiDiMixin,
		AbstractCoreActionsMixin
):
	"""
	Mixin providing high-level interaction capabilities for Core WebDrivers.

	Includes factories for standard and human-like ActionChains, as well as
	custom WebDriverWait implementations.
	"""
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	def action_chains(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	):
		raise NotImplementedExperimentalFeatureError(name="CoreActionsMixin.action_chains")
	
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
		
		return get_trio_bidi_instance_wrapper(
				wrapper_class=WebDriverWait,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
				trio_token=self._trio_token,
				bidi_buffer_size=self._trio_bidi_buffer_size,
		)
