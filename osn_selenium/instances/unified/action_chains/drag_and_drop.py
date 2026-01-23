from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.unified.action_chains.base import UnifiedBaseMixin
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["UnifiedDragAndDropMixin"]


class UnifiedDragAndDropMixin(UnifiedBaseMixin):
	def _drag_and_drop_by_offset_impl(self, source: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> legacyActionChains:
		return self._legacy_impl.drag_and_drop_by_offset(
				source=get_legacy_instance(instance=source),
				xoffset=xoffset,
				yoffset=yoffset
		)
	
	def _drag_and_drop_impl(self, source: WEB_ELEMENT_TYPEHINT, target: WEB_ELEMENT_TYPEHINT) -> legacyActionChains:
		return self._legacy_impl.drag_and_drop(
				source=get_legacy_instance(instance=source),
				target=get_legacy_instance(instance=target)
		)
