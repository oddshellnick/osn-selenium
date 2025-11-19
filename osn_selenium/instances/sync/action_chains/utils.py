from typing import TYPE_CHECKING, Union
from osn_selenium.instances.sync.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.utils import UnifiedUtilsMixin
from osn_selenium.abstract.instances.action_chains.utils import AbstractUtilsMixin


__all__ = ["UtilsMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class UtilsMixin(BaseMixin, UnifiedUtilsMixin, AbstractUtilsMixin):
	"""
	Mixin class providing utility methods for action chains.
	"""
	
	def pause(self, seconds: Union[float, int]) -> "ActionChains":
		action_chains = self._pause_impl(seconds=seconds)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def perform(self) -> None:
		self._perform_impl()
	
	def reset_actions(self) -> None:
		self._reset_actions_impl()
