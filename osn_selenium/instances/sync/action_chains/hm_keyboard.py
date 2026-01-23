from typing import TYPE_CHECKING
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.sync.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.hm_keyboard import (
	UnifiedHMKeyboardMixin
)
from osn_selenium.abstract.instances.action_chains.hm_keyboard import (
	AbstractHMKeyboardMixin
)


__all__ = ["HMKeyboardMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class HMKeyboardMixin(BaseMixin, UnifiedHMKeyboardMixin, AbstractHMKeyboardMixin):
	"""
	Mixin class providing human-like keyboard interaction methods.
	"""
	
	def hm_send_keys(self, text: str) -> "ActionChains":
		action_chains = self._hm_send_keys_impl(text=text)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def hm_send_keys_to_element(self, element: WEB_ELEMENT_TYPEHINT, text: str) -> "ActionChains":
		action_chains = self._hm_send_keys_to_element_impl(element=element, text=text)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
