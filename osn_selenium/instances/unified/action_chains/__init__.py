from osn_selenium.instances.unified.action_chains.click import UnifiedClickMixin
from osn_selenium.instances.unified.action_chains.hm_move import UnifiedHMMoveMixin
from osn_selenium.instances.unified.action_chains.hm_scroll import UnifiedHMScrollMixin
from osn_selenium.instances.unified.action_chains.hm_keyboard import (
	UnifiedHMKeyboardMixin
)
from osn_selenium.instances.unified.action_chains.drag_and_drop import (
	UnifiedDragAndDropMixin
)


__all__ = ["UnifiedActionChains"]


class UnifiedActionChains(
		UnifiedClickMixin,
		UnifiedDragAndDropMixin,
		UnifiedHMKeyboardMixin,
		UnifiedHMMoveMixin,
		UnifiedHMScrollMixin,
):
	pass
