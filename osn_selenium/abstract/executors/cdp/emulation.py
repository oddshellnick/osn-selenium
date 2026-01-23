from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractEmulationCDPExecutor"]


class AbstractEmulationCDPExecutor(ABC):
	@abstractmethod
	def add_screen(
			self,
			left: int,
			top: int,
			width: int,
			height: int,
			work_area_insets: Optional[Dict[str, Any]] = None,
			device_pixel_ratio: Optional[float] = None,
			rotation: Optional[int] = None,
			color_depth: Optional[int] = None,
			label: Optional[str] = None,
			is_internal: Optional[bool] = None
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def can_emulate(self) -> bool:
		...
	
	@abstractmethod
	def clear_device_metrics_override(self) -> None:
		...
	
	@abstractmethod
	def clear_device_posture_override(self) -> None:
		...
	
	@abstractmethod
	def clear_display_features_override(self) -> None:
		...
	
	@abstractmethod
	def clear_geolocation_override(self) -> None:
		...
	
	@abstractmethod
	def clear_idle_override(self) -> None:
		...
	
	@abstractmethod
	def get_overridden_sensor_information(self, type_: str) -> float:
		...
	
	@abstractmethod
	def get_screen_infos(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def remove_screen(self, screen_id: str) -> None:
		...
	
	@abstractmethod
	def reset_page_scale_factor(self) -> None:
		...
	
	@abstractmethod
	def set_auto_dark_mode_override(self, enabled: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def set_automation_override(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_cpu_throttling_rate(self, rate: float) -> None:
		...
	
	@abstractmethod
	def set_data_saver_override(self, data_saver_enabled: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def set_default_background_color_override(self, color: Optional[Dict[str, Any]] = None) -> None:
		...
	
	@abstractmethod
	def set_device_metrics_override(
			self,
			width: int,
			height: int,
			device_scale_factor: float,
			mobile: bool,
			scale: Optional[float] = None,
			screen_width: Optional[int] = None,
			screen_height: Optional[int] = None,
			position_x: Optional[int] = None,
			position_y: Optional[int] = None,
			dont_set_visible_size: Optional[bool] = None,
			screen_orientation: Optional[Dict[str, Any]] = None,
			viewport: Optional[Dict[str, Any]] = None,
			display_feature: Optional[Dict[str, Any]] = None,
			device_posture: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_device_posture_override(self, posture: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def set_disabled_image_types(self, image_types: List[str]) -> None:
		...
	
	@abstractmethod
	def set_display_features_override(self, features: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_document_cookie_disabled(self, disabled: bool) -> None:
		...
	
	@abstractmethod
	def set_emit_touch_events_for_mouse(self, enabled: bool, configuration: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_emulated_media(
			self,
			media: Optional[str] = None,
			features: Optional[List[Dict[str, Any]]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_emulated_os_text_scale(self, scale: Optional[float] = None) -> None:
		...
	
	@abstractmethod
	def set_emulated_vision_deficiency(self, type_: str) -> None:
		...
	
	@abstractmethod
	def set_focus_emulation_enabled(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_geolocation_override(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None,
			altitude: Optional[float] = None,
			altitude_accuracy: Optional[float] = None,
			heading: Optional[float] = None,
			speed: Optional[float] = None
	) -> None:
		...
	
	@abstractmethod
	def set_hardware_concurrency_override(self, hardware_concurrency: int) -> None:
		...
	
	@abstractmethod
	def set_idle_override(self, is_user_active: bool, is_screen_unlocked: bool) -> None:
		...
	
	@abstractmethod
	def set_locale_override(self, locale: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_navigator_overrides(self, platform: str) -> None:
		...
	
	@abstractmethod
	def set_page_scale_factor(self, page_scale_factor: float) -> None:
		...
	
	@abstractmethod
	def set_pressure_data_override(
			self,
			source: str,
			state: str,
			own_contribution_estimate: Optional[float] = None
	) -> None:
		...
	
	@abstractmethod
	def set_pressure_source_override_enabled(
			self,
			enabled: bool,
			source: str,
			metadata: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_pressure_state_override(self, source: str, state: str) -> None:
		...
	
	@abstractmethod
	def set_safe_area_insets_override(self, insets: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def set_script_execution_disabled(self, value: bool) -> None:
		...
	
	@abstractmethod
	def set_scrollbars_hidden(self, hidden: bool) -> None:
		...
	
	@abstractmethod
	def set_sensor_override_enabled(self, enabled: bool, type_: str, metadata: Optional[Dict[str, Any]] = None) -> None:
		...
	
	@abstractmethod
	def set_sensor_override_readings(self, type_: str, reading: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def set_small_viewport_height_difference_override(self, difference: int) -> None:
		...
	
	@abstractmethod
	def set_timezone_override(self, timezone_id: str) -> None:
		...
	
	@abstractmethod
	def set_touch_emulation_enabled(self, enabled: bool, max_touch_points: Optional[int] = None) -> None:
		...
	
	@abstractmethod
	def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_virtual_time_policy(
			self,
			policy: str,
			budget: Optional[float] = None,
			max_virtual_time_task_starvation_count: Optional[int] = None,
			initial_virtual_time: Optional[float] = None
	) -> float:
		...
	
	@abstractmethod
	def set_visible_size(self, width: int, height: int) -> None:
		...
