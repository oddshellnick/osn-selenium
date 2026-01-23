from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedEmulationCDPExecutor"]


class UnifiedEmulationCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_screen_impl(
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
		return self._execute_function(
				"Emulation.addScreen",
				{
					"left": left,
					"top": top,
					"width": width,
					"height": height,
					"work_area_insets": work_area_insets,
					"device_pixel_ratio": device_pixel_ratio,
					"rotation": rotation,
					"color_depth": color_depth,
					"label": label,
					"is_internal": is_internal
				}
		)
	
	def _can_emulate_impl(self) -> bool:
		return self._execute_function("Emulation.canEmulate", {})
	
	def _clear_device_metrics_override_impl(self) -> None:
		return self._execute_function("Emulation.clearDeviceMetricsOverride", {})
	
	def _clear_device_posture_override_impl(self) -> None:
		return self._execute_function("Emulation.clearDevicePostureOverride", {})
	
	def _clear_display_features_override_impl(self) -> None:
		return self._execute_function("Emulation.clearDisplayFeaturesOverride", {})
	
	def _clear_geolocation_override_impl(self) -> None:
		return self._execute_function("Emulation.clearGeolocationOverride", {})
	
	def _clear_idle_override_impl(self) -> None:
		return self._execute_function("Emulation.clearIdleOverride", {})
	
	def _get_overridden_sensor_information_impl(self, type_: str) -> float:
		return self._execute_function("Emulation.getOverriddenSensorInformation", {"type_": type_})
	
	def _get_screen_infos_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Emulation.getScreenInfos", {})
	
	def _remove_screen_impl(self, screen_id: str) -> None:
		return self._execute_function("Emulation.removeScreen", {"screen_id": screen_id})
	
	def _reset_page_scale_factor_impl(self) -> None:
		return self._execute_function("Emulation.resetPageScaleFactor", {})
	
	def _set_auto_dark_mode_override_impl(self, enabled: Optional[bool] = None) -> None:
		return self._execute_function("Emulation.setAutoDarkModeOverride", {"enabled": enabled})
	
	def _set_automation_override_impl(self, enabled: bool) -> None:
		return self._execute_function("Emulation.setAutomationOverride", {"enabled": enabled})
	
	def _set_cpu_throttling_rate_impl(self, rate: float) -> None:
		return self._execute_function("Emulation.setCPUThrottlingRate", {"rate": rate})
	
	def _set_data_saver_override_impl(self, data_saver_enabled: Optional[bool] = None) -> None:
		return self._execute_function(
				"Emulation.setDataSaverOverride",
				{"data_saver_enabled": data_saver_enabled}
		)
	
	def _set_default_background_color_override_impl(self, color: Optional[Dict[str, Any]] = None) -> None:
		return self._execute_function("Emulation.setDefaultBackgroundColorOverride", {"color": color})
	
	def _set_device_metrics_override_impl(
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
		return self._execute_function(
				"Emulation.setDeviceMetricsOverride",
				{
					"width": width,
					"height": height,
					"device_scale_factor": device_scale_factor,
					"mobile": mobile,
					"scale": scale,
					"screen_width": screen_width,
					"screen_height": screen_height,
					"position_x": position_x,
					"position_y": position_y,
					"dont_set_visible_size": dont_set_visible_size,
					"screen_orientation": screen_orientation,
					"viewport": viewport,
					"display_feature": display_feature,
					"device_posture": device_posture
				}
		)
	
	def _set_device_posture_override_impl(self, posture: Dict[str, Any]) -> None:
		return self._execute_function("Emulation.setDevicePostureOverride", {"posture": posture})
	
	def _set_disabled_image_types_impl(self, image_types: List[str]) -> None:
		return self._execute_function("Emulation.setDisabledImageTypes", {"image_types": image_types})
	
	def _set_display_features_override_impl(self, features: List[Dict[str, Any]]) -> None:
		return self._execute_function("Emulation.setDisplayFeaturesOverride", {"features": features})
	
	def _set_document_cookie_disabled_impl(self, disabled: bool) -> None:
		return self._execute_function("Emulation.setDocumentCookieDisabled", {"disabled": disabled})
	
	def _set_emit_touch_events_for_mouse_impl(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return self._execute_function(
				"Emulation.setEmitTouchEventsForMouse",
				{"enabled": enabled, "configuration": configuration}
		)
	
	def _set_emulated_media_impl(
			self,
			media: Optional[str] = None,
			features: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._execute_function("Emulation.setEmulatedMedia", {"media": media, "features": features})
	
	def _set_emulated_os_text_scale_impl(self, scale: Optional[float] = None) -> None:
		return self._execute_function("Emulation.setEmulatedOSTextScale", {"scale": scale})
	
	def _set_emulated_vision_deficiency_impl(self, type_: str) -> None:
		return self._execute_function("Emulation.setEmulatedVisionDeficiency", {"type_": type_})
	
	def _set_focus_emulation_enabled_impl(self, enabled: bool) -> None:
		return self._execute_function("Emulation.setFocusEmulationEnabled", {"enabled": enabled})
	
	def _set_geolocation_override_impl(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None,
			altitude: Optional[float] = None,
			altitude_accuracy: Optional[float] = None,
			heading: Optional[float] = None,
			speed: Optional[float] = None
	) -> None:
		return self._execute_function(
				"Emulation.setGeolocationOverride",
				{
					"latitude": latitude,
					"longitude": longitude,
					"accuracy": accuracy,
					"altitude": altitude,
					"altitude_accuracy": altitude_accuracy,
					"heading": heading,
					"speed": speed
				}
		)
	
	def _set_hardware_concurrency_override_impl(self, hardware_concurrency: int) -> None:
		return self._execute_function(
				"Emulation.setHardwareConcurrencyOverride",
				{"hardware_concurrency": hardware_concurrency}
		)
	
	def _set_idle_override_impl(self, is_user_active: bool, is_screen_unlocked: bool) -> None:
		return self._execute_function(
				"Emulation.setIdleOverride",
				{
					"is_user_active": is_user_active,
					"is_screen_unlocked": is_screen_unlocked
				}
		)
	
	def _set_locale_override_impl(self, locale: Optional[str] = None) -> None:
		return self._execute_function("Emulation.setLocaleOverride", {"locale": locale})
	
	def _set_navigator_overrides_impl(self, platform: str) -> None:
		return self._execute_function("Emulation.setNavigatorOverrides", {"platform": platform})
	
	def _set_page_scale_factor_impl(self, page_scale_factor: float) -> None:
		return self._execute_function("Emulation.setPageScaleFactor", {"page_scale_factor": page_scale_factor})
	
	def _set_pressure_data_override_impl(
			self,
			source: str,
			state: str,
			own_contribution_estimate: Optional[float] = None
	) -> None:
		return self._execute_function(
				"Emulation.setPressureDataOverride",
				{
					"source": source,
					"state": state,
					"own_contribution_estimate": own_contribution_estimate
				}
		)
	
	def _set_pressure_source_override_enabled_impl(
			self,
			enabled: bool,
			source: str,
			metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Emulation.setPressureSourceOverrideEnabled",
				{"enabled": enabled, "source": source, "metadata": metadata}
		)
	
	def _set_pressure_state_override_impl(self, source: str, state: str) -> None:
		return self._execute_function("Emulation.setPressureStateOverride", {"source": source, "state": state})
	
	def _set_safe_area_insets_override_impl(self, insets: Dict[str, Any]) -> None:
		return self._execute_function("Emulation.setSafeAreaInsetsOverride", {"insets": insets})
	
	def _set_script_execution_disabled_impl(self, value: bool) -> None:
		return self._execute_function("Emulation.setScriptExecutionDisabled", {"value": value})
	
	def _set_scrollbars_hidden_impl(self, hidden: bool) -> None:
		return self._execute_function("Emulation.setScrollbarsHidden", {"hidden": hidden})
	
	def _set_sensor_override_enabled_impl(self, enabled: bool, type_: str, metadata: Optional[Dict[str, Any]] = None) -> None:
		return self._execute_function(
				"Emulation.setSensorOverrideEnabled",
				{"enabled": enabled, "type_": type_, "metadata": metadata}
		)
	
	def _set_sensor_override_readings_impl(self, type_: str, reading: Dict[str, Any]) -> None:
		return self._execute_function(
				"Emulation.setSensorOverrideReadings",
				{"type_": type_, "reading": reading}
		)
	
	def _set_small_viewport_height_difference_override_impl(self, difference: int) -> None:
		return self._execute_function(
				"Emulation.setSmallViewportHeightDifferenceOverride",
				{"difference": difference}
		)
	
	def _set_timezone_override_impl(self, timezone_id: str) -> None:
		return self._execute_function("Emulation.setTimezoneOverride", {"timezone_id": timezone_id})
	
	def _set_touch_emulation_enabled_impl(self, enabled: bool, max_touch_points: Optional[int] = None) -> None:
		return self._execute_function(
				"Emulation.setTouchEmulationEnabled",
				{"enabled": enabled, "max_touch_points": max_touch_points}
		)
	
	def _set_user_agent_override_impl(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Emulation.setUserAgentOverride",
				{
					"user_agent": user_agent,
					"accept_language": accept_language,
					"platform": platform,
					"user_agent_metadata": user_agent_metadata
				}
		)
	
	def _set_virtual_time_policy_impl(
			self,
			policy: str,
			budget: Optional[float] = None,
			max_virtual_time_task_starvation_count: Optional[int] = None,
			initial_virtual_time: Optional[float] = None
	) -> float:
		return self._execute_function(
				"Emulation.setVirtualTimePolicy",
				{
					"policy": policy,
					"budget": budget,
					"max_virtual_time_task_starvation_count": max_virtual_time_task_starvation_count,
					"initial_virtual_time": initial_virtual_time
				}
		)
	
	def _set_visible_size_impl(self, width: int, height: int) -> None:
		return self._execute_function("Emulation.setVisibleSize", {"width": width, "height": height})
