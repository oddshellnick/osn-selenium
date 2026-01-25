from typing import Optional
from osn_selenium.models import Point
from osn_selenium.instances._functions import scroll_to_parts
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from osn_selenium.instances.unified.action_chains.utils import UnifiedUtilsMixin
from osn_selenium.instances.unified.action_chains.scroll import UnifiedScrollMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedHMScrollMixin"]


class UnifiedHMScrollMixin(UnifiedUtilsMixin, UnifiedScrollMixin):
	def _hm_scroll_from_origin_impl(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None) -> legacyActionChains:
		if origin is None:
			viewport_size = self._js_executor._get_viewport_size_impl()
		
			origin_x = 0 if delta_x >= 0 else viewport_size.width
			origin_y = 0 if delta_y >= 0 else viewport_size.height
		
			origin = ScrollOrigin.from_viewport(x_offset=origin_x, y_offset=origin_y)
		
		start = Point(x=int(origin.x_offset), y=int(origin.y_offset))
		end = Point(x=int(origin.x_offset) + int(delta_x), y=int(origin.y_offset) + int(delta_y))
		
		parts = scroll_to_parts(start_position=start, end_position=end)
		
		for part in parts:
			self._pause_impl(seconds=part.duration * 0.001)
			self._scroll_from_origin_impl(scroll_origin=origin, delta_x=int(part.delta.x), delta_y=int(part.delta.y))
		
		return self._legacy_impl
	
	def _hm_scroll_by_amount_impl(self, delta_x: int, delta_y: int) -> legacyActionChains:
		start = Point(x=0, y=0)
		end = Point(x=int(delta_x), y=int(delta_y))
		
		parts = scroll_to_parts(start_position=start, end_position=end)
		
		for part in parts:
			self._pause_impl(seconds=part.duration * 0.001)
			self._scroll_by_amount_impl(delta_x=int(part.delta.x), delta_y=int(part.delta.y))
		
		return self._legacy_impl
	
	def _hm_scroll_to_element_impl(
			self,
			element: WEB_ELEMENT_TYPEHINT,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
	) -> legacyActionChains:
		viewport_rect = self._js_executor._get_viewport_rect_impl()
		element_rect = self._js_executor._get_element_rect_in_viewport_impl(element=get_legacy_instance(instance=element))
		
		if element_rect.x < additional_left_x_offset:
			delta_x = int(element_rect.x - additional_left_x_offset)
		elif element_rect.x + element_rect.width > viewport_rect.width - additional_right_x_offset:
			delta_x = int(
					element_rect.x + element_rect.width - (viewport_rect.width - additional_right_x_offset)
			)
		else:
			delta_x = 0
		
		if element_rect.y < additional_upper_y_offset:
			delta_y = int(element_rect.y - additional_upper_y_offset)
		elif element_rect.y + element_rect.height > viewport_rect.height - additional_lower_y_offset:
			delta_y = int(
					element_rect.y + element_rect.height - (viewport_rect.height - additional_lower_y_offset)
			)
		else:
			delta_y = 0
		
		return self._hm_scroll_by_amount_impl(delta_x=delta_x, delta_y=delta_y)
