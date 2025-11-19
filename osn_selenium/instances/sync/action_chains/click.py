from typing import (
	Optional,
	TYPE_CHECKING
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.sync.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.click import UnifiedClickMixin
from osn_selenium.abstract.instances.action_chains.click import AbstractClickMixin


__all__ = ["ClickMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class ClickMixin(BaseMixin, UnifiedClickMixin, AbstractClickMixin):
	"""
	Mixin class providing mouse click interaction methods.
	"""
	
	def click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "ActionChains":
		action_chains = self._click_impl(on_element=get_legacy_instance(instance=on_element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def click_and_hold(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "ActionChains":
		action_chains = self._click_and_hold_impl(on_element=get_legacy_instance(instance=on_element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def context_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "ActionChains":
		action_chains = self._context_click_impl(on_element=get_legacy_instance(instance=on_element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def double_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "ActionChains":
		action_chains = self._double_click_impl(on_element=get_legacy_instance(instance=on_element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def release(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "ActionChains":
		action_chains = self._release_impl(on_element=get_legacy_instance(instance=on_element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
