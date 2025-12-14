from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.emulation import (
	AbstractEmulationCDPExecutor
)


class EmulationCDPExecutor(AbstractEmulationCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def add_screen(
			self,
			left: int,
			top: int,
			width: int,
			height: int,
			work_area_insets: Optional[Any] = None,
			device_pixel_ratio: Optional[float] = None,
			rotation: Optional[int] = None,
			color_depth: Optional[int] = None,
			label: Optional[str] = None,
			is_internal: Optional[bool] = None
	) -> Any:
		return self._execute_function("Emulation.addScreen", locals())
	
	def can_emulate(self) -> bool:
		return self._execute_function("Emulation.canEmulate", locals())
	
	def clear_device_metrics_override(self) -> None:
		return self._execute_function("Emulation.clearDeviceMetricsOverride", locals())
	
	def clear_device_posture_override(self) -> None:
		return self._execute_function("Emulation.clearDevicePostureOverride", locals())
	
	def clear_display_features_override(self) -> None:
		return self._execute_function("Emulation.clearDisplayFeaturesOverride", locals())
	
	def clear_geolocation_override(self) -> None:
		return self._execute_function("Emulation.clearGeolocationOverride", locals())
	
	def clear_idle_override(self) -> None:
		return self._execute_function("Emulation.clearIdleOverride", locals())
	
	def get_overridden_sensor_information(self, type_: str) -> float:
		return self._execute_function("Emulation.getOverriddenSensorInformation", locals())
	
	def get_screen_infos(self) -> List[Any]:
		return self._execute_function("Emulation.getScreenInfos", locals())
	
	def remove_screen(self, screen_id: str) -> None:
		return self._execute_function("Emulation.removeScreen", locals())
	
	def reset_page_scale_factor(self) -> None:
		return self._execute_function("Emulation.resetPageScaleFactor", locals())
	
	def set_auto_dark_mode_override(self, enabled: Optional[bool] = None) -> None:
		return self._execute_function("Emulation.setAutoDarkModeOverride", locals())
	
	def set_automation_override(self, enabled: bool) -> None:
		return self._execute_function("Emulation.setAutomationOverride", locals())
	
	def set_cpu_throttling_rate(self, rate: float) -> None:
		return self._execute_function("Emulation.setCPUThrottlingRate", locals())
	
	def set_data_saver_override(self, data_saver_enabled: Optional[bool] = None) -> None:
		return self._execute_function("Emulation.setDataSaverOverride", locals())
	
	def set_default_background_color_override(self, color: Optional[Any] = None) -> None:
		return self._execute_function("Emulation.setDefaultBackgroundColorOverride", locals())
	
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
			screen_orientation: Optional[Any] = None,
			viewport: Optional[Any] = None,
			display_feature: Optional[Any] = None,
			device_posture: Optional[Any] = None
	) -> None:
		return self._execute_function("Emulation.setDeviceMetricsOverride", locals())
	
	def set_device_posture_override(self, posture: Any) -> None:
		return self._execute_function("Emulation.setDevicePostureOverride", locals())
	
	def set_disabled_image_types(self, image_types: List[str]) -> None:
		return self._execute_function("Emulation.setDisabledImageTypes", locals())
	
	def set_display_features_override(self, features: List[Any]) -> None:
		return self._execute_function("Emulation.setDisplayFeaturesOverride", locals())
	
	def set_document_cookie_disabled(self, disabled: bool) -> None:
		return self._execute_function("Emulation.setDocumentCookieDisabled", locals())
	
	def set_emit_touch_events_for_mouse(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return self._execute_function("Emulation.setEmitTouchEventsForMouse", locals())
	
	def set_emulated_media(self, media: Optional[str] = None, features: Optional[List[Any]] = None) -> None:
		return self._execute_function("Emulation.setEmulatedMedia", locals())
	
	def set_emulated_os_text_scale(self, scale: Optional[float] = None) -> None:
		return self._execute_function("Emulation.setEmulatedOSTextScale", locals())
	
	def set_emulated_vision_deficiency(self, type_: str) -> None:
		return self._execute_function("Emulation.setEmulatedVisionDeficiency", locals())
	
	def set_focus_emulation_enabled(self, enabled: bool) -> None:
		return self._execute_function("Emulation.setFocusEmulationEnabled", locals())
	
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
		return self._execute_function("Emulation.setGeolocationOverride", locals())
	
	def set_hardware_concurrency_override(self, hardware_concurrency: int) -> None:
		return self._execute_function("Emulation.setHardwareConcurrencyOverride", locals())
	
	def set_idle_override(self, is_user_active: bool, is_screen_unlocked: bool) -> None:
		return self._execute_function("Emulation.setIdleOverride", locals())
	
	def set_locale_override(self, locale: Optional[str] = None) -> None:
		return self._execute_function("Emulation.setLocaleOverride", locals())
	
	def set_navigator_overrides(self, platform: str) -> None:
		return self._execute_function("Emulation.setNavigatorOverrides", locals())
	
	def set_page_scale_factor(self, page_scale_factor: float) -> None:
		return self._execute_function("Emulation.setPageScaleFactor", locals())
	
	def set_pressure_data_override(
			self,
			source: str,
			state: str,
			own_contribution_estimate: Optional[float] = None
	) -> None:
		return self._execute_function("Emulation.setPressureDataOverride", locals())
	
	def set_pressure_source_override_enabled(self, enabled: bool, source: str, metadata: Optional[Any] = None) -> None:
		return self._execute_function("Emulation.setPressureSourceOverrideEnabled", locals())
	
	def set_pressure_state_override(self, source: str, state: str) -> None:
		return self._execute_function("Emulation.setPressureStateOverride", locals())
	
	def set_safe_area_insets_override(self, insets: Any) -> None:
		return self._execute_function("Emulation.setSafeAreaInsetsOverride", locals())
	
	def set_script_execution_disabled(self, value: bool) -> None:
		return self._execute_function("Emulation.setScriptExecutionDisabled", locals())
	
	def set_scrollbars_hidden(self, hidden: bool) -> None:
		return self._execute_function("Emulation.setScrollbarsHidden", locals())
	
	def set_sensor_override_enabled(self, enabled: bool, type_: str, metadata: Optional[Any] = None) -> None:
		return self._execute_function("Emulation.setSensorOverrideEnabled", locals())
	
	def set_sensor_override_readings(self, type_: str, reading: Any) -> None:
		return self._execute_function("Emulation.setSensorOverrideReadings", locals())
	
	def set_small_viewport_height_difference_override(self, difference: int) -> None:
		return self._execute_function("Emulation.setSmallViewportHeightDifferenceOverride", locals())
	
	def set_timezone_override(self, timezone_id: str) -> None:
		return self._execute_function("Emulation.setTimezoneOverride", locals())
	
	def set_touch_emulation_enabled(self, enabled: bool, max_touch_points: Optional[int] = None) -> None:
		return self._execute_function("Emulation.setTouchEmulationEnabled", locals())
	
	def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Any] = None
	) -> None:
		return self._execute_function("Emulation.setUserAgentOverride", locals())
	
	def set_virtual_time_policy(
			self,
			policy: str,
			budget: Optional[float] = None,
			max_virtual_time_task_starvation_count: Optional[int] = None,
			initial_virtual_time: Optional[float] = None
	) -> float:
		return self._execute_function("Emulation.setVirtualTimePolicy", locals())
	
	def set_visible_size(self, width: int, height: int) -> None:
		return self._execute_function("Emulation.setVisibleSize", locals())
