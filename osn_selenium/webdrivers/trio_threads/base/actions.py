from typing import List, Optional
from osn_selenium.types import DEVICES_TYPEHINT
from osn_selenium.webdrivers.decorators import requires_driver
from selenium.webdriver import (
	ActionChains as legacyActionChains
)
from osn_selenium.webdrivers.trio_threads.base.script import ScriptMixin
from osn_selenium.abstract.webdriver.base.actions import AbstractActionsMixin
from osn_selenium.instances.trio_threads.action_chains import (
	ActionChains,
	HumanLikeActionChains
)


class ActionsMixin(ScriptMixin, AbstractActionsMixin):
	@requires_driver
	async def action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> ActionChains:
		return ActionChains(
				legacyActionChains(driver=self.driver, duration=duration, devices=devices),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> HumanLikeActionChains:
		return HumanLikeActionChains(
				execute_script_function=self.execute_script,
				selenium_action_chains=legacyActionChains(driver=self.driver, duration=duration, devices=devices),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
