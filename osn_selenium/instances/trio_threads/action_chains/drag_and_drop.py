from typing import TYPE_CHECKING
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.trio_threads.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.drag_and_drop import (
	UnifiedDragAndDropMixin
)
from osn_selenium.abstract.instances.action_chains.drag_and_drop import (
	AbstractDragAndDropMixin
)


if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.action_chains import ActionChains


class DragAndDropMixin(BaseMixin, UnifiedDragAndDropMixin, AbstractDragAndDropMixin):
	"""
	Mixin class providing drag and drop interaction methods.
	"""
	
	async def drag_and_drop(self, source: WEB_ELEMENT_TYPEHINT, target: WEB_ELEMENT_TYPEHINT) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._drag_and_drop_impl)(source=get_legacy_instance(source), target=get_legacy_instance(target))
		
		return self.from_legacy(
				selenium_action_chains=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def drag_and_drop_by_offset(self, source: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._drag_and_drop_by_offset_impl)(source=get_legacy_instance(source), xoffset=xoffset, yoffset=yoffset)
		
		return self.from_legacy(
				selenium_action_chains=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
