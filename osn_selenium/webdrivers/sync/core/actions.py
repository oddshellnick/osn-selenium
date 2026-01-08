from osn_selenium.types import DEVICES_TYPEHINT
from typing import (
	Iterable,
	List,
	Optional
)
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.core.script import CoreScriptMixin
from osn_selenium.instances.sync.web_driver_wait import WebDriverWait
from selenium.webdriver import (
	ActionChains as legacyActionChains
)
from osn_selenium.abstract.webdriver.core.actions import AbstractCoreActionsMixin
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)
from osn_selenium.instances.sync.action_chains import (
	ActionChains,
	HumanLikeActionChains
)


class CoreActionsMixin(CoreScriptMixin, AbstractCoreActionsMixin):
	@requires_driver
	def action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> ActionChains:
		return ActionChains(
				selenium_action_chains=legacyActionChains(driver=self.driver, duration=duration, devices=devices),
		)
	
	@requires_driver
	def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> HumanLikeActionChains:
		return HumanLikeActionChains(
				execute_script_function=self.execute_script,
				selenium_action_chains=legacyActionChains(driver=self.driver, duration=duration, devices=devices),
		)
	
	@requires_driver
	def web_driver_wait(
			self,
			timeout: float,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Iterable[BaseException]] = None,
	) -> WebDriverWait:
		return WebDriverWait(
				selenium_webdriver_wait=legacyWebDriverWait(
						driver=self.driver,
						timeout=timeout,
						poll_frequency=poll_frequency,
						ignored_exceptions=ignored_exceptions,
				),
		)
