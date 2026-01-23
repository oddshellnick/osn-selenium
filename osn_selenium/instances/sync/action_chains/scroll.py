from typing import TYPE_CHECKING
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.sync.action_chains.base import BaseMixin
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from osn_selenium.instances.unified.action_chains.scroll import UnifiedScrollMixin
from osn_selenium.abstract.instances.action_chains.scroll import AbstractScrollMixin


__all__ = ["ScrollMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class ScrollMixin(BaseMixin, UnifiedScrollMixin, AbstractScrollMixin):
	"""
	Mixin class providing scroll and wheel interaction methods.
	"""
	
	def scroll_by_amount(self, delta_x: int, delta_y: int) -> "ActionChains":
		action_chains = self._scroll_by_amount_impl(delta_x=delta_x, delta_y=delta_y)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int) -> "ActionChains":
		action_chains = self._scroll_from_origin_impl(scroll_origin=scroll_origin, delta_x=delta_x, delta_y=delta_y)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def scroll_to_element(self, element: WEB_ELEMENT_TYPEHINT) -> "ActionChains":
		action_chains = self._scroll_to_element_impl(element=get_legacy_instance(instance=element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
