from typing import TYPE_CHECKING, Union
from osn_selenium.instances.trio_threads.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.utils import UnifiedUtilsMixin
from osn_selenium.abstract.instances.action_chains.utils import AbstractUtilsMixin


__all__ = ["UtilsMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.action_chains import ActionChains


class UtilsMixin(BaseMixin, UnifiedUtilsMixin, AbstractUtilsMixin):
	"""
	Mixin class providing utility methods for action chains.
	"""
	
	async def pause(self, seconds: Union[float, int]) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._pause_impl)(seconds=seconds)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def perform(self) -> None:
		await self.sync_to_trio(sync_function=self._perform_impl)()
	
	async def reset_actions(self) -> None:
		await self.sync_to_trio(sync_function=self._reset_actions_impl)()
