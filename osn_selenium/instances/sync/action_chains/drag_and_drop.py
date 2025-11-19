from typing import TYPE_CHECKING
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.sync.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.drag_and_drop import (
	UnifiedDragAndDropMixin
)
from osn_selenium.abstract.instances.action_chains.drag_and_drop import (
	AbstractDragAndDropMixin
)


__all__ = ["DragAndDropMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.action_chains import ActionChains


class DragAndDropMixin(BaseMixin, UnifiedDragAndDropMixin, AbstractDragAndDropMixin):
	"""
	Mixin class providing drag and drop interaction methods.
	"""
	
	def drag_and_drop(self, source: WEB_ELEMENT_TYPEHINT, target: WEB_ELEMENT_TYPEHINT) -> "ActionChains":
		action_chains = self._drag_and_drop_impl(
				source=get_legacy_instance(instance=source),
				target=get_legacy_instance(instance=target)
		)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
	
	def drag_and_drop_by_offset(self, source: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> "ActionChains":
		action_chains = self._drag_and_drop_by_offset_impl(
				source=get_legacy_instance(instance=source),
				xoffset=xoffset,
				yoffset=yoffset
		)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
		)
