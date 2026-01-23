from osn_selenium.models import Point
from typing import TYPE_CHECKING, Tuple
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.trio_threads.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.hm_move import UnifiedHMMoveMixin
from osn_selenium.abstract.instances.action_chains.hm_move import AbstractHMMoveMixin


__all__ = ["HMMoveMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.action_chains import ActionChains


class HMMoveMixin(BaseMixin, UnifiedHMMoveMixin, AbstractHMMoveMixin):
	"""
	Mixin class providing human-like mouse movement interaction methods.
	"""
	
	async def hm_move(self, start_position: Point, end_position: Point) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._hm_move_impl)(start_position=start_position, end_position=end_position)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def hm_move_by_offset(self, start_position: Point, xoffset: int, yoffset: int) -> Tuple["ActionChains", Point]:
		action_chains, point = await self.sync_to_trio(sync_function=self._hm_move_by_offset_impl)(start_position=start_position, xoffset=xoffset, yoffset=yoffset)
		
		return (
				self.from_legacy(
						legacy_object=action_chains,
						execute_js_script_function=self._execute_js_script_function,
						lock=self._lock,
						limiter=self._capacity_limiter,
				),
				point,
		)
	
	async def hm_move_to_element(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple["ActionChains", Point]:
		action_chains, point = await self.sync_to_trio(sync_function=self._hm_move_to_element_impl)(start_position=start_position, element=element)
		
		return (
				self.from_legacy(
						legacy_object=action_chains,
						execute_js_script_function=self._execute_js_script_function,
						lock=self._lock,
						limiter=self._capacity_limiter,
				),
				point,
		)
	
	async def hm_move_to_element_with_offset(
			self,
			start_position: Point,
			element: WEB_ELEMENT_TYPEHINT,
			xoffset: int,
			yoffset: int
	) -> Tuple["ActionChains", Point]:
		action_chains, point = await self.sync_to_trio(sync_function=self._hm_move_to_element_with_offset_impl)(
				start_position=start_position,
				element=element,
				xoffset=xoffset,
				yoffset=yoffset,
		)
		
		return (
				self.from_legacy(
						legacy_object=action_chains,
						execute_js_script_function=self._execute_js_script_function,
						lock=self._lock,
						limiter=self._capacity_limiter,
				),
				point,
		)
	
	async def hm_move_to_element_with_random_offset(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple["ActionChains", Point]:
		action_chains, point = await self.sync_to_trio(sync_function=self._hm_move_to_element_with_random_offset_impl)(start_position=start_position, element=element)
		
		return (
				self.from_legacy(
						legacy_object=action_chains,
						execute_js_script_function=self._execute_js_script_function,
						lock=self._lock,
						limiter=self._capacity_limiter,
				),
				point,
		)
