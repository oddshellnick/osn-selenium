from typing import (
	Optional,
	TYPE_CHECKING
)
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from osn_selenium.instances.trio_threads.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.hm_scroll import UnifiedHMScrollMixin
from osn_selenium.abstract.instances.action_chains.hm_scroll import (
	AbstractHMScrollMixin
)


__all__ = ["HMScrollMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.action_chains import ActionChains


class HMScrollMixin(BaseMixin, UnifiedHMScrollMixin, AbstractHMScrollMixin):
	"""
	Mixin class providing human-like scroll interaction methods.
	"""
	
	async def hm_scroll_by_amount(self, delta_x: int, delta_y: int) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._hm_scroll_by_amount_impl)(delta_x=delta_x, delta_y=delta_y)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def hm_scroll_from_origin(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._hm_scroll_from_origin_impl)(delta_x=delta_x, delta_y=delta_y, origin=origin)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def hm_scroll_to_element(
			self,
			element: WEB_ELEMENT_TYPEHINT,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
	) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._hm_scroll_to_element_impl)(
				element=element,
				additional_lower_y_offset=additional_lower_y_offset,
				additional_upper_y_offset=additional_upper_y_offset,
				additional_right_x_offset=additional_right_x_offset,
				additional_left_x_offset=additional_left_x_offset,
		)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
