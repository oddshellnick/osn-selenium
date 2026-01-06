from typing import List, Optional
from osn_selenium.types import DEVICES_TYPEHINT
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.base.script import ScriptMixin
from selenium.webdriver import (
	ActionChains as legacyActionChains
)
from osn_selenium.abstract.webdriver.base.actions import AbstractActionsMixin
from osn_selenium.instances.sync.action_chains import (
	ActionChains,
	HumanLikeActionChains
)


class ActionsMixin(ScriptMixin, AbstractActionsMixin):
	@requires_driver
	def action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> ActionChains:
		return ActionChains(
				legacyActionChains(driver=self.driver, duration=duration, devices=devices),
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
