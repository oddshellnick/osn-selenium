from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.emulation import (
	UnifiedEmulationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.emulation import (
	AbstractEmulationCDPExecutor
)


__all__ = ["EmulationCDPExecutor"]


class EmulationCDPExecutor(UnifiedEmulationCDPExecutor, AbstractEmulationCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedEmulationCDPExecutor.__init__(self, execute_function=execute_function)
	
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
		return self._add_screen_impl(
				left=left,
				top=top,
				width=width,
				height=height,
				work_area_insets=work_area_insets,
				device_pixel_ratio=device_pixel_ratio,
				rotation=rotation,
				color_depth=color_depth,
				label=label,
				is_internal=is_internal
		)
	
	def can_emulate(self) -> bool:
		return self._can_emulate_impl()
	
	def clear_device_metrics_override(self) -> None:
		return self._clear_device_metrics_override_impl()
	
	def clear_device_posture_override(self) -> None:
		return self._clear_device_posture_override_impl()
	
	def clear_display_features_override(self) -> None:
		return self._clear_display_features_override_impl()
	
	def clear_geolocation_override(self) -> None:
		return self._clear_geolocation_override_impl()
	
	def clear_idle_override(self) -> None:
		return self._clear_idle_override_impl()
	
	def get_overridden_sensor_information(self, type_: str) -> float:
		return self._get_overridden_sensor_information_impl(type_=type_)
	
	def get_screen_infos(self) -> List[Dict[str, Any]]:
		return self._get_screen_infos_impl()
	
	def remove_screen(self, screen_id: str) -> None:
		return self._remove_screen_impl(screen_id=screen_id)
	
	def reset_page_scale_factor(self) -> None:
		return self._reset_page_scale_factor_impl()
	
	def set_auto_dark_mode_override(self, enabled: Optional[bool] = None) -> None:
		return self._set_auto_dark_mode_override_impl(enabled=enabled)
	
	def set_automation_override(self, enabled: bool) -> None:
		return self._set_automation_override_impl(enabled=enabled)
	
	def set_cpu_throttling_rate(self, rate: float) -> None:
		return self._set_cpu_throttling_rate_impl(rate=rate)
	
	def set_data_saver_override(self, data_saver_enabled: Optional[bool] = None) -> None:
		return self._set_data_saver_override_impl(data_saver_enabled=data_saver_enabled)
	
	def set_default_background_color_override(self, color: Optional[Dict[str, Any]] = None) -> None:
		return self._set_default_background_color_override_impl(color=color)
	
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
		return self._set_device_metrics_override_impl(
				width=width,
				height=height,
				device_scale_factor=device_scale_factor,
				mobile=mobile,
				scale=scale,
				screen_width=screen_width,
				screen_height=screen_height,
				position_x=position_x,
				position_y=position_y,
				dont_set_visible_size=dont_set_visible_size,
				screen_orientation=screen_orientation,
				viewport=viewport,
				display_feature=display_feature,
				device_posture=device_posture
		)
	
	def set_device_posture_override(self, posture: Dict[str, Any]) -> None:
		return self._set_device_posture_override_impl(posture=posture)
	
	def set_disabled_image_types(self, image_types: List[str]) -> None:
		return self._set_disabled_image_types_impl(image_types=image_types)
	
	def set_display_features_override(self, features: List[Dict[str, Any]]) -> None:
		return self._set_display_features_override_impl(features=features)
	
	def set_document_cookie_disabled(self, disabled: bool) -> None:
		return self._set_document_cookie_disabled_impl(disabled=disabled)
	
	def set_emit_touch_events_for_mouse(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return self._set_emit_touch_events_for_mouse_impl(enabled=enabled, configuration=configuration)
	
	def set_emulated_media(
			self,
			media: Optional[str] = None,
			features: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._set_emulated_media_impl(media=media, features=features)
	
	def set_emulated_os_text_scale(self, scale: Optional[float] = None) -> None:
		return self._set_emulated_os_text_scale_impl(scale=scale)
	
	def set_emulated_vision_deficiency(self, type_: str) -> None:
		return self._set_emulated_vision_deficiency_impl(type_=type_)
	
	def set_focus_emulation_enabled(self, enabled: bool) -> None:
		return self._set_focus_emulation_enabled_impl(enabled=enabled)
	
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
		return self._set_geolocation_override_impl(
				latitude=latitude,
				longitude=longitude,
				accuracy=accuracy,
				altitude=altitude,
				altitude_accuracy=altitude_accuracy,
				heading=heading,
				speed=speed
		)
	
	def set_hardware_concurrency_override(self, hardware_concurrency: int) -> None:
		return self._set_hardware_concurrency_override_impl(hardware_concurrency=hardware_concurrency)
	
	def set_idle_override(self, is_user_active: bool, is_screen_unlocked: bool) -> None:
		return self._set_idle_override_impl(is_user_active=is_user_active, is_screen_unlocked=is_screen_unlocked)
	
	def set_locale_override(self, locale: Optional[str] = None) -> None:
		return self._set_locale_override_impl(locale=locale)
	
	def set_navigator_overrides(self, platform: str) -> None:
		return self._set_navigator_overrides_impl(platform=platform)
	
	def set_page_scale_factor(self, page_scale_factor: float) -> None:
		return self._set_page_scale_factor_impl(page_scale_factor=page_scale_factor)
	
	def set_pressure_data_override(
			self,
			source: str,
			state: str,
			own_contribution_estimate: Optional[float] = None
	) -> None:
		return self._set_pressure_data_override_impl(
				source=source,
				state=state,
				own_contribution_estimate=own_contribution_estimate
		)
	
	def set_pressure_source_override_enabled(
			self,
			enabled: bool,
			source: str,
			metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return self._set_pressure_source_override_enabled_impl(enabled=enabled, source=source, metadata=metadata)
	
	def set_pressure_state_override(self, source: str, state: str) -> None:
		return self._set_pressure_state_override_impl(source=source, state=state)
	
	def set_safe_area_insets_override(self, insets: Dict[str, Any]) -> None:
		return self._set_safe_area_insets_override_impl(insets=insets)
	
	def set_script_execution_disabled(self, value: bool) -> None:
		return self._set_script_execution_disabled_impl(value=value)
	
	def set_scrollbars_hidden(self, hidden: bool) -> None:
		return self._set_scrollbars_hidden_impl(hidden=hidden)
	
	def set_sensor_override_enabled(self, enabled: bool, type_: str, metadata: Optional[Dict[str, Any]] = None) -> None:
		return self._set_sensor_override_enabled_impl(enabled=enabled, type_=type_, metadata=metadata)
	
	def set_sensor_override_readings(self, type_: str, reading: Dict[str, Any]) -> None:
		return self._set_sensor_override_readings_impl(type_=type_, reading=reading)
	
	def set_small_viewport_height_difference_override(self, difference: int) -> None:
		return self._set_small_viewport_height_difference_override_impl(difference=difference)
	
	def set_timezone_override(self, timezone_id: str) -> None:
		return self._set_timezone_override_impl(timezone_id=timezone_id)
	
	def set_touch_emulation_enabled(self, enabled: bool, max_touch_points: Optional[int] = None) -> None:
		return self._set_touch_emulation_enabled_impl(enabled=enabled, max_touch_points=max_touch_points)
	
	def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return self._set_user_agent_override_impl(
				user_agent=user_agent,
				accept_language=accept_language,
				platform=platform,
				user_agent_metadata=user_agent_metadata
		)
	
	def set_virtual_time_policy(
			self,
			policy: str,
			budget: Optional[float] = None,
			max_virtual_time_task_starvation_count: Optional[int] = None,
			initial_virtual_time: Optional[float] = None
	) -> float:
		return self._set_virtual_time_policy_impl(
				policy=policy,
				budget=budget,
				max_virtual_time_task_starvation_count=max_virtual_time_task_starvation_count,
				initial_virtual_time=initial_virtual_time
		)
	
	def set_visible_size(self, width: int, height: int) -> None:
		return self._set_visible_size_impl(width=width, height=height)
