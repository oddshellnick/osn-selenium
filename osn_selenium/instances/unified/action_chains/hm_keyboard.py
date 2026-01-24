from osn_selenium.instances._functions import text_input_to_parts
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.unified.action_chains.utils import UnifiedUtilsMixin
from osn_selenium.instances.unified.action_chains.keyboard import UnifiedKeyboardMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedHMKeyboardMixin"]


class UnifiedHMKeyboardMixin(UnifiedUtilsMixin, UnifiedKeyboardMixin):
	def _hm_send_keys_impl(self, text: str) -> legacyActionChains:
		parts = text_input_to_parts(text=text)
		
		for part in parts:
			self._pause_impl(seconds=part.duration * 0.001)
			self._send_keys_impl(part.text)
		
		return self._legacy_impl
	
	def _hm_send_keys_to_element_impl(self, element: WEB_ELEMENT_TYPEHINT, text: str) -> legacyActionChains:
		parts = text_input_to_parts(text=text)
		
		for part in parts:
			self._pause_impl(seconds=part.duration * 0.001)
			self._send_keys_to_element_impl(element, part.text)
		
		return self._legacy_impl
