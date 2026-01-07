from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.emulation import (
	AbstractEmulationCDPExecutor
)


class EmulationCDPExecutor(AbstractEmulationCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_screen(
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
		return await self._execute_function("Emulation.addScreen", locals())
	
	async def can_emulate(self) -> bool:
		return await self._execute_function("Emulation.canEmulate", locals())
	
	async def clear_device_metrics_override(self) -> None:
		return await self._execute_function("Emulation.clearDeviceMetricsOverride", locals())
	
	async def clear_device_posture_override(self) -> None:
		return await self._execute_function("Emulation.clearDevicePostureOverride", locals())
	
	async def clear_display_features_override(self) -> None:
		return await self._execute_function("Emulation.clearDisplayFeaturesOverride", locals())
	
	async def clear_geolocation_override(self) -> None:
		return await self._execute_function("Emulation.clearGeolocationOverride", locals())
	
	async def clear_idle_override(self) -> None:
		return await self._execute_function("Emulation.clearIdleOverride", locals())
	
	async def get_overridden_sensor_information(self, type_: str) -> float:
		return await self._execute_function("Emulation.getOverriddenSensorInformation", locals())
	
	async def get_screen_infos(self) -> List[Any]:
		return await self._execute_function("Emulation.getScreenInfos", locals())
	
	async def remove_screen(self, screen_id: str) -> None:
		return await self._execute_function("Emulation.removeScreen", locals())
	
	async def reset_page_scale_factor(self) -> None:
		return await self._execute_function("Emulation.resetPageScaleFactor", locals())
	
	async def set_auto_dark_mode_override(self, enabled: Optional[bool] = None) -> None:
		return await self._execute_function("Emulation.setAutoDarkModeOverride", locals())
	
	async def set_automation_override(self, enabled: bool) -> None:
		return await self._execute_function("Emulation.setAutomationOverride", locals())
	
	async def set_cpu_throttling_rate(self, rate: float) -> None:
		return await self._execute_function("Emulation.setCPUThrottlingRate", locals())
	
	async def set_data_saver_override(self, data_saver_enabled: Optional[bool] = None) -> None:
		return await self._execute_function("Emulation.setDataSaverOverride", locals())
	
	async def set_default_background_color_override(self, color: Optional[Any] = None) -> None:
		return await self._execute_function("Emulation.setDefaultBackgroundColorOverride", locals())
	
	async def set_device_metrics_override(
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
		return await self._execute_function("Emulation.setDeviceMetricsOverride", locals())
	
	async def set_device_posture_override(self, posture: Any) -> None:
		return await self._execute_function("Emulation.setDevicePostureOverride", locals())
	
	async def set_disabled_image_types(self, image_types: List[str]) -> None:
		return await self._execute_function("Emulation.setDisabledImageTypes", locals())
	
	async def set_display_features_override(self, features: List[Any]) -> None:
		return await self._execute_function("Emulation.setDisplayFeaturesOverride", locals())
	
	async def set_document_cookie_disabled(self, disabled: bool) -> None:
		return await self._execute_function("Emulation.setDocumentCookieDisabled", locals())
	
	async def set_emit_touch_events_for_mouse(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return await self._execute_function("Emulation.setEmitTouchEventsForMouse", locals())
	
	async def set_emulated_media(self, media: Optional[str] = None, features: Optional[List[Any]] = None) -> None:
		return await self._execute_function("Emulation.setEmulatedMedia", locals())
	
	async def set_emulated_os_text_scale(self, scale: Optional[float] = None) -> None:
		return await self._execute_function("Emulation.setEmulatedOSTextScale", locals())
	
	async def set_emulated_vision_deficiency(self, type_: str) -> None:
		return await self._execute_function("Emulation.setEmulatedVisionDeficiency", locals())
	
	async def set_focus_emulation_enabled(self, enabled: bool) -> None:
		return await self._execute_function("Emulation.setFocusEmulationEnabled", locals())
	
	async def set_geolocation_override(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None,
			altitude: Optional[float] = None,
			altitude_accuracy: Optional[float] = None,
			heading: Optional[float] = None,
			speed: Optional[float] = None
	) -> None:
		return await self._execute_function("Emulation.setGeolocationOverride", locals())
	
	async def set_hardware_concurrency_override(self, hardware_concurrency: int) -> None:
		return await self._execute_function("Emulation.setHardwareConcurrencyOverride", locals())
	
	async def set_idle_override(self, is_user_active: bool, is_screen_unlocked: bool) -> None:
		return await self._execute_function("Emulation.setIdleOverride", locals())
	
	async def set_locale_override(self, locale: Optional[str] = None) -> None:
		return await self._execute_function("Emulation.setLocaleOverride", locals())
	
	async def set_navigator_overrides(self, platform: str) -> None:
		return await self._execute_function("Emulation.setNavigatorOverrides", locals())
	
	async def set_page_scale_factor(self, page_scale_factor: float) -> None:
		return await self._execute_function("Emulation.setPageScaleFactor", locals())
	
	async def set_pressure_data_override(
			self,
			source: str,
			state: str,
			own_contribution_estimate: Optional[float] = None
	) -> None:
		return await self._execute_function("Emulation.setPressureDataOverride", locals())
	
	async def set_pressure_source_override_enabled(self, enabled: bool, source: str, metadata: Optional[Any] = None) -> None:
		return await self._execute_function("Emulation.setPressureSourceOverrideEnabled", locals())
	
	async def set_pressure_state_override(self, source: str, state: str) -> None:
		return await self._execute_function("Emulation.setPressureStateOverride", locals())
	
	async def set_safe_area_insets_override(self, insets: Any) -> None:
		return await self._execute_function("Emulation.setSafeAreaInsetsOverride", locals())
	
	async def set_script_execution_disabled(self, value: bool) -> None:
		return await self._execute_function("Emulation.setScriptExecutionDisabled", locals())
	
	async def set_scrollbars_hidden(self, hidden: bool) -> None:
		return await self._execute_function("Emulation.setScrollbarsHidden", locals())
	
	async def set_sensor_override_enabled(self, enabled: bool, type_: str, metadata: Optional[Any] = None) -> None:
		return await self._execute_function("Emulation.setSensorOverrideEnabled", locals())
	
	async def set_sensor_override_readings(self, type_: str, reading: Any) -> None:
		return await self._execute_function("Emulation.setSensorOverrideReadings", locals())
	
	async def set_small_viewport_height_difference_override(self, difference: int) -> None:
		return await self._execute_function("Emulation.setSmallViewportHeightDifferenceOverride", locals())
	
	async def set_timezone_override(self, timezone_id: str) -> None:
		return await self._execute_function("Emulation.setTimezoneOverride", locals())
	
	async def set_touch_emulation_enabled(self, enabled: bool, max_touch_points: Optional[int] = None) -> None:
		return await self._execute_function("Emulation.setTouchEmulationEnabled", locals())
	
	async def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Any] = None
	) -> None:
		return await self._execute_function("Emulation.setUserAgentOverride", locals())
	
	async def set_virtual_time_policy(
			self,
			policy: str,
			budget: Optional[float] = None,
			max_virtual_time_task_starvation_count: Optional[int] = None,
			initial_virtual_time: Optional[float] = None
	) -> float:
		return await self._execute_function("Emulation.setVirtualTimePolicy", locals())
	
	async def set_visible_size(self, width: int, height: int) -> None:
		return await self._execute_function("Emulation.setVisibleSize", locals())
