from typing import Union
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedUtilsMixin"]


class UnifiedUtilsMixin(UnifiedBaseMixin):
	def _pause_impl(self, seconds: Union[float, int]) -> legacyActionChains:
		return self._legacy_impl.pause(seconds=seconds)
	
	def _perform_impl(self) -> None:
		self._legacy_impl.perform()
	
	def _reset_actions_impl(self) -> None:
		self._legacy_impl.reset_actions()
