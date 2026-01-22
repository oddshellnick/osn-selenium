from typing import TYPE_CHECKING
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from osn_selenium.instances.trio_threads.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.scroll import UnifiedScrollMixin
from osn_selenium.abstract.instances.action_chains.scroll import AbstractScrollMixin


if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.action_chains import ActionChains


class ScrollMixin(BaseMixin, UnifiedScrollMixin, AbstractScrollMixin):
	"""
	Mixin class providing scroll and wheel interaction methods.
	"""
	
	async def scroll_by_amount(self, delta_x: int, delta_y: int) -> "ActionChains":
		action_chains = await self._sync_to_trio(self._scroll_by_amount_impl, delta_x=delta_x, delta_y=delta_y)
		
		return self.from_legacy(
				selenium_action_chains=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int) -> "ActionChains":
		action_chains = await self._sync_to_trio(
				self._scroll_from_origin_impl,
				scroll_origin=scroll_origin,
				delta_x=delta_x,
				delta_y=delta_y,
		)
		
		return self.from_legacy(
				selenium_action_chains=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def scroll_to_element(self, element: WEB_ELEMENT_TYPEHINT) -> "ActionChains":
		action_chains = await self._sync_to_trio(self._scroll_to_element_impl, element=get_legacy_instance(element))
		
		return self.from_legacy(
				selenium_action_chains=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
