from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractInputCDPExecutor"]


class AbstractInputCDPExecutor(ABC):
	@abstractmethod
	def cancel_dragging(self) -> None:
		...
	
	@abstractmethod
	def dispatch_drag_event(
			self,
			type_: str,
			x: float,
			y: float,
			data: Dict[str, Any],
			modifiers: Optional[int] = None
	) -> None:
		...
	
	@abstractmethod
	def dispatch_key_event(
			self,
			type_: str,
			modifiers: Optional[int] = None,
			timestamp: Optional[float] = None,
			text: Optional[str] = None,
			unmodified_text: Optional[str] = None,
			key_identifier: Optional[str] = None,
			code: Optional[str] = None,
			key: Optional[str] = None,
			windows_virtual_key_code: Optional[int] = None,
			native_virtual_key_code: Optional[int] = None,
			auto_repeat: Optional[bool] = None,
			is_keypad: Optional[bool] = None,
			is_system_key: Optional[bool] = None,
			location: Optional[int] = None,
			commands: Optional[List[str]] = None
	) -> None:
		...
	
	@abstractmethod
	def dispatch_mouse_event(
			self,
			type_: str,
			x: float,
			y: float,
			modifiers: Optional[int] = None,
			timestamp: Optional[float] = None,
			button: Optional[str] = None,
			buttons: Optional[int] = None,
			click_count: Optional[int] = None,
			force: Optional[float] = None,
			tangential_pressure: Optional[float] = None,
			tilt_x: Optional[float] = None,
			tilt_y: Optional[float] = None,
			twist: Optional[int] = None,
			delta_x: Optional[float] = None,
			delta_y: Optional[float] = None,
			pointer_type: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def dispatch_touch_event(
			self,
			type_: str,
			touch_points: List[Dict[str, Any]],
			modifiers: Optional[int] = None,
			timestamp: Optional[float] = None
	) -> None:
		...
	
	@abstractmethod
	def emulate_touch_from_mouse_event(
			self,
			type_: str,
			x: int,
			y: int,
			button: str,
			timestamp: Optional[float] = None,
			delta_x: Optional[float] = None,
			delta_y: Optional[float] = None,
			modifiers: Optional[int] = None,
			click_count: Optional[int] = None
	) -> None:
		...
	
	@abstractmethod
	def ime_set_composition(
			self,
			text: str,
			selection_start: int,
			selection_end: int,
			replacement_start: Optional[int] = None,
			replacement_end: Optional[int] = None
	) -> None:
		...
	
	@abstractmethod
	def insert_text(self, text: str) -> None:
		...
	
	@abstractmethod
	def set_ignore_input_events(self, ignore: bool) -> None:
		...
	
	@abstractmethod
	def set_intercept_drags(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def synthesize_pinch_gesture(
			self,
			x: float,
			y: float,
			scale_factor: float,
			relative_speed: Optional[int] = None,
			gesture_source_type: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def synthesize_scroll_gesture(
			self,
			x: float,
			y: float,
			x_distance: Optional[float] = None,
			y_distance: Optional[float] = None,
			x_overscroll: Optional[float] = None,
			y_overscroll: Optional[float] = None,
			prevent_fling: Optional[bool] = None,
			speed: Optional[int] = None,
			gesture_source_type: Optional[str] = None,
			repeat_count: Optional[int] = None,
			repeat_delay_ms: Optional[int] = None,
			interaction_marker_name: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def synthesize_tap_gesture(
			self,
			x: float,
			y: float,
			duration: Optional[int] = None,
			tap_count: Optional[int] = None,
			gesture_source_type: Optional[str] = None
	) -> None:
		...
