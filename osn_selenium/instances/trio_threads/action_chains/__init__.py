from osn_selenium.instances.trio_threads.action_chains.move import MoveMixin
from osn_selenium.abstract.instances.action_chains import AbstractActionChains
from osn_selenium.instances.trio_threads.action_chains.click import ClickMixin
from osn_selenium.instances.trio_threads.action_chains.utils import UtilsMixin
from osn_selenium.instances.trio_threads.action_chains.scroll import ScrollMixin
from osn_selenium.instances.trio_threads.action_chains.hm_move import HMMoveMixin
from osn_selenium.instances.trio_threads.action_chains.keyboard import KeyboardMixin
from osn_selenium.instances.trio_threads.action_chains.hm_scroll import HMScrollMixin
from osn_selenium.instances.trio_threads.action_chains.hm_keyboard import HMKeyboardMixin
from osn_selenium.instances.trio_threads.action_chains.drag_and_drop import DragAndDropMixin


__all__ = ["ActionChains"]


class ActionChains(
		ClickMixin,
		DragAndDropMixin,
		UtilsMixin,
		HMKeyboardMixin,
		HMMoveMixin,
		HMScrollMixin,
		KeyboardMixin,
		MoveMixin,
		ScrollMixin,
		AbstractActionChains,
):
	"""
	ActionChains class combining standard and human-like interaction mixins.
	"""
	
	pass
