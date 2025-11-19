from typing import Optional
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedKeyboardMixin"]


class UnifiedKeyboardMixin(UnifiedBaseMixin):
	def _key_down_impl(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.key_down(value=value, element=get_legacy_instance(instance=element))
	
	def _key_up_impl(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.key_up(value=value, element=get_legacy_instance(instance=element))
	
	def _send_keys_impl(self, *keys_to_send: str) -> legacyActionChains:
		return self._legacy_impl.send_keys(*keys_to_send)
	
	def _send_keys_to_element_impl(self, element: WEB_ELEMENT_TYPEHINT, *keys_to_send: str) -> legacyActionChains:
		return self._legacy_impl.send_keys_to_element(get_legacy_instance(instance=element), *keys_to_send)
