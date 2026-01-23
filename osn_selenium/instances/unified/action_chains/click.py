from typing import Optional
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedClickMixin"]


class UnifiedClickMixin(UnifiedBaseMixin):
	def _click_and_hold_impl(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.click_and_hold(on_element=get_legacy_instance(instance=on_element))
	
	def _click_impl(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.click(on_element=get_legacy_instance(instance=on_element))
	
	def _context_click_impl(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.context_click(on_element=get_legacy_instance(instance=on_element))
	
	def _double_click_impl(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.double_click(on_element=get_legacy_instance(instance=on_element))
	
	def _release_impl(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> legacyActionChains:
		return self._legacy_impl.release(on_element=get_legacy_instance(instance=on_element))
