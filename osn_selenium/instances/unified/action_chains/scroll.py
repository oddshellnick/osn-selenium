from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedScrollMixin"]


class UnifiedScrollMixin(UnifiedBaseMixin):
	def _scroll_by_amount_impl(self, delta_x: int, delta_y: int) -> legacyActionChains:
		return self._legacy_impl.scroll_by_amount(delta_x=delta_x, delta_y=delta_y)
	
	def _scroll_from_origin_impl(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int) -> legacyActionChains:
		return self._legacy_impl.scroll_from_origin(scroll_origin=scroll_origin, delta_x=delta_x, delta_y=delta_y)
	
	def _scroll_to_element_impl(self, element: WEB_ELEMENT_TYPEHINT) -> legacyActionChains:
		return self._legacy_impl.scroll_to_element(element=get_legacy_instance(instance=element))
