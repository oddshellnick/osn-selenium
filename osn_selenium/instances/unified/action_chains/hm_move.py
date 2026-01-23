from typing import Tuple
from osn_selenium.models import Point
from osn_selenium.instances._functions import move_to_parts
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.exceptions.instance import (
	ElementNotVisibleError
)
from osn_selenium.instances.unified.web_element import UnifiedWebElement
from osn_selenium.instances.unified.action_chains.move import UnifiedMoveMixin
from osn_selenium.instances.unified.action_chains.utils import UnifiedUtilsMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedHMMoveMixin"]


class UnifiedHMMoveMixin(UnifiedUtilsMixin, UnifiedMoveMixin):
	def _hm_move_impl(self, start_position: Point, end_position: Point) -> legacyActionChains:
		parts = move_to_parts(start_position=start_position, end_position=end_position)
		
		for part in parts:
			self._pause_impl(seconds=part.duration * 0.001)
			self._move_by_offset_impl(xoffset=part.offset.x, yoffset=part.offset.y)
		
		return self._legacy_impl
	
	def _hm_move_by_offset_impl(self, start_position: Point, xoffset: int, yoffset: int) -> Tuple[legacyActionChains, Point]:
		end_position = Point(x=start_position.x + xoffset, y=start_position.y + yoffset)
		
		return self._hm_move_impl(start_position=start_position, end_position=end_position), end_position
	
	def _hm_move_to_element_impl(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple[legacyActionChains, Point]:
		element_rect = UnifiedWebElement(selenium_web_element=get_legacy_instance(instance=element))._rect_impl()
		end_position = Point(
				x=element_rect["x"] +
				element_rect["width"] //
				2,
				y=element_rect["y"] +
				element_rect["height"] //
				2
		)
		
		return self._hm_move_impl(start_position=start_position, end_position=end_position), end_position
	
	def _hm_move_to_element_with_offset_impl(
			self,
			start_position: Point,
			element: WEB_ELEMENT_TYPEHINT,
			xoffset: int,
			yoffset: int
	) -> Tuple[legacyActionChains, Point]:
		element_rect = UnifiedWebElement(selenium_web_element=get_legacy_instance(instance=element))._rect_impl()
		end_position = Point(x=element_rect["x"] + xoffset, y=element_rect["y"] + yoffset)
		
		return self._hm_move_impl(start_position=start_position, end_position=end_position), end_position
	
	def _hm_move_to_element_with_random_offset_impl(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple[legacyActionChains, Point]:
		end_position = self._js_executor._get_random_element_point_impl(element=get_legacy_instance(instance=element))
		
		if end_position is None:
			raise ElementNotVisibleError(element_id=get_legacy_instance(instance=element).id)
		
		return self._hm_move_impl(start_position=start_position, end_position=end_position), end_position
