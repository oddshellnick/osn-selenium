from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedMoveMixin"]


class UnifiedMoveMixin(UnifiedBaseMixin):
	def _move_by_offset_impl(self, xoffset: int, yoffset: int) -> legacyActionChains:
		return self._legacy_impl.move_by_offset(xoffset=xoffset, yoffset=yoffset)
	
	def _move_to_element_impl(self, to_element: WEB_ELEMENT_TYPEHINT) -> legacyActionChains:
		return self._legacy_impl.move_to_element(to_element=get_legacy_instance(instance=to_element))
	
	def _move_to_element_with_offset_impl(self, to_element: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> legacyActionChains:
		return self._legacy_impl.move_to_element_with_offset(
				to_element=get_legacy_instance(instance=to_element),
				xoffset=xoffset,
				yoffset=yoffset
		)
