from typing import TYPE_CHECKING
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.sync.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.move import UnifiedMoveMixin
from osn_selenium.abstract.instances.action_chains.move import AbstractMoveMixin


__all__ = ["MoveMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class MoveMixin(BaseMixin, UnifiedMoveMixin, AbstractMoveMixin):
	"""
	Mixin class providing mouse movement interaction methods.
	"""
	
	def move_by_offset(self, xoffset: int, yoffset: int) -> "ActionChains":
		action_chains = self._move_by_offset_impl(xoffset=xoffset, yoffset=yoffset)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def move_to_element(self, to_element: WEB_ELEMENT_TYPEHINT) -> "ActionChains":
		action_chains = self._move_to_element_impl(to_element=get_legacy_instance(instance=to_element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def move_to_element_with_offset(self, to_element: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> "ActionChains":
		action_chains = self._move_to_element_with_offset_impl(
				to_element=get_legacy_instance(instance=to_element),
				xoffset=xoffset,
				yoffset=yoffset
		)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
