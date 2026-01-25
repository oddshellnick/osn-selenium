from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.input import (
	UnifiedInputCDPExecutor
)
from osn_selenium.abstract.executors.cdp.input import (
	AbstractInputCDPExecutor
)


__all__ = ["InputCDPExecutor"]


class InputCDPExecutor(UnifiedInputCDPExecutor, AbstractInputCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedInputCDPExecutor.__init__(self, execute_function=execute_function)
	
	def cancel_dragging(self) -> None:
		return self._cancel_dragging_impl()
	
	def dispatch_drag_event(
			self,
			type_: str,
			x: float,
			y: float,
			data: Dict[str, Any],
			modifiers: Optional[int] = None
	) -> None:
		return self._dispatch_drag_event_impl(type_=type_, x=x, y=y, data=data, modifiers=modifiers)
	
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
		return self._dispatch_key_event_impl(
				type_=type_,
				modifiers=modifiers,
				timestamp=timestamp,
				text=text,
				unmodified_text=unmodified_text,
				key_identifier=key_identifier,
				code=code,
				key=key,
				windows_virtual_key_code=windows_virtual_key_code,
				native_virtual_key_code=native_virtual_key_code,
				auto_repeat=auto_repeat,
				is_keypad=is_keypad,
				is_system_key=is_system_key,
				location=location,
				commands=commands
		)
	
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
		return self._dispatch_mouse_event_impl(
				type_=type_,
				x=x,
				y=y,
				modifiers=modifiers,
				timestamp=timestamp,
				button=button,
				buttons=buttons,
				click_count=click_count,
				force=force,
				tangential_pressure=tangential_pressure,
				tilt_x=tilt_x,
				tilt_y=tilt_y,
				twist=twist,
				delta_x=delta_x,
				delta_y=delta_y,
				pointer_type=pointer_type
		)
	
	def dispatch_touch_event(
			self,
			type_: str,
			touch_points: List[Dict[str, Any]],
			modifiers: Optional[int] = None,
			timestamp: Optional[float] = None
	) -> None:
		return self._dispatch_touch_event_impl(
				type_=type_,
				touch_points=touch_points,
				modifiers=modifiers,
				timestamp=timestamp
		)
	
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
		return self._emulate_touch_from_mouse_event_impl(
				type_=type_,
				x=x,
				y=y,
				button=button,
				timestamp=timestamp,
				delta_x=delta_x,
				delta_y=delta_y,
				modifiers=modifiers,
				click_count=click_count
		)
	
	def ime_set_composition(
			self,
			text: str,
			selection_start: int,
			selection_end: int,
			replacement_start: Optional[int] = None,
			replacement_end: Optional[int] = None
	) -> None:
		return self._ime_set_composition_impl(
				text=text,
				selection_start=selection_start,
				selection_end=selection_end,
				replacement_start=replacement_start,
				replacement_end=replacement_end
		)
	
	def insert_text(self, text: str) -> None:
		return self._insert_text_impl(text=text)
	
	def set_ignore_input_events(self, ignore: bool) -> None:
		return self._set_ignore_input_events_impl(ignore=ignore)
	
	def set_intercept_drags(self, enabled: bool) -> None:
		return self._set_intercept_drags_impl(enabled=enabled)
	
	def synthesize_pinch_gesture(
			self,
			x: float,
			y: float,
			scale_factor: float,
			relative_speed: Optional[int] = None,
			gesture_source_type: Optional[str] = None
	) -> None:
		return self._synthesize_pinch_gesture_impl(
				x=x,
				y=y,
				scale_factor=scale_factor,
				relative_speed=relative_speed,
				gesture_source_type=gesture_source_type
		)
	
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
		return self._synthesize_scroll_gesture_impl(
				x=x,
				y=y,
				x_distance=x_distance,
				y_distance=y_distance,
				x_overscroll=x_overscroll,
				y_overscroll=y_overscroll,
				prevent_fling=prevent_fling,
				speed=speed,
				gesture_source_type=gesture_source_type,
				repeat_count=repeat_count,
				repeat_delay_ms=repeat_delay_ms,
				interaction_marker_name=interaction_marker_name
		)
	
	def synthesize_tap_gesture(
			self,
			x: float,
			y: float,
			duration: Optional[int] = None,
			tap_count: Optional[int] = None,
			gesture_source_type: Optional[str] = None
	) -> None:
		return self._synthesize_tap_gesture_impl(
				x=x,
				y=y,
				duration=duration,
				tap_count=tap_count,
				gesture_source_type=gesture_source_type
		)
