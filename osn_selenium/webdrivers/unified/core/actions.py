from typing import (
	Iterable,
	List,
	Optional
)
from osn_selenium._typehints import DEVICES_TYPEHINT
from osn_selenium.webdrivers._decorators import requires_driver
from selenium.webdriver import (
	ActionChains as legacyActionChains
)
from osn_selenium.webdrivers.unified.core.script import (
	UnifiedCoreScriptMixin
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)


__all__ = ["UnifiedCoreActionsMixin"]


class UnifiedCoreActionsMixin(UnifiedCoreScriptMixin):
	@requires_driver
	def _action_chains_impl(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> legacyActionChains:
		return legacyActionChains(driver=self._driver_impl, duration=duration, devices=devices)
	
	@requires_driver
	def _web_driver_wait_impl(
			self,
			timeout: float,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Iterable[BaseException]] = None,
	) -> legacyWebDriverWait:
		return legacyWebDriverWait(
				driver=self._driver_impl,
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
