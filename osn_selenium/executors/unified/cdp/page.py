from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedPageCDPExecutor"]


class UnifiedPageCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_compilation_cache_impl(self, url: str, data: str) -> None:
		return self._execute_function("Page.addCompilationCache", {"url": url, "data": data})
	
	def _add_script_to_evaluate_on_load_impl(self, script_source: str) -> str:
		return self._execute_function("Page.addScriptToEvaluateOnLoad", {"script_source": script_source})
	
	def _add_script_to_evaluate_on_new_document_impl(
			self,
			source: str,
			world_name: Optional[str] = None,
			include_command_line_api: Optional[bool] = None,
			run_immediately: Optional[bool] = None
	) -> str:
		return self._execute_function(
				"Page.addScriptToEvaluateOnNewDocument",
				{
					"source": source,
					"world_name": world_name,
					"include_command_line_api": include_command_line_api,
					"run_immediately": run_immediately
				}
		)
	
	def _bring_to_front_impl(self) -> None:
		return self._execute_function("Page.bringToFront", {})
	
	def _capture_screenshot_impl(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			clip: Optional[Dict[str, Any]] = None,
			from_surface: Optional[bool] = None,
			capture_beyond_viewport: Optional[bool] = None,
			optimize_for_speed: Optional[bool] = None
	) -> str:
		return self._execute_function(
				"Page.captureScreenshot",
				{
					"format_": format_,
					"quality": quality,
					"clip": clip,
					"from_surface": from_surface,
					"capture_beyond_viewport": capture_beyond_viewport,
					"optimize_for_speed": optimize_for_speed
				}
		)
	
	def _capture_snapshot_impl(self, format_: Optional[str] = None) -> str:
		return self._execute_function("Page.captureSnapshot", {"format_": format_})
	
	def _clear_compilation_cache_impl(self) -> None:
		return self._execute_function("Page.clearCompilationCache", {})
	
	def _clear_device_metrics_override_impl(self) -> None:
		return self._execute_function("Page.clearDeviceMetricsOverride", {})
	
	def _clear_device_orientation_override_impl(self) -> None:
		return self._execute_function("Page.clearDeviceOrientationOverride", {})
	
	def _clear_geolocation_override_impl(self) -> None:
		return self._execute_function("Page.clearGeolocationOverride", {})
	
	def _close_impl(self) -> None:
		return self._execute_function("Page.close", {})
	
	def _crash_impl(self) -> None:
		return self._execute_function("Page.crash", {})
	
	def _create_isolated_world_impl(
			self,
			frame_id: str,
			world_name: Optional[str] = None,
			grant_univeral_access: Optional[bool] = None
	) -> int:
		return self._execute_function(
				"Page.createIsolatedWorld",
				{
					"frame_id": frame_id,
					"world_name": world_name,
					"grant_univeral_access": grant_univeral_access
				}
		)
	
	def _delete_cookie_impl(self, cookie_name: str, url: str) -> None:
		return self._execute_function("Page.deleteCookie", {"cookie_name": cookie_name, "url": url})
	
	def _disable_impl(self) -> None:
		return self._execute_function("Page.disable", {})
	
	def _enable_impl(self, enable_file_chooser_opened_event: Optional[bool] = None) -> None:
		return self._execute_function(
				"Page.enable",
				{"enable_file_chooser_opened_event": enable_file_chooser_opened_event}
		)
	
	def _generate_test_report_impl(self, message: str, group: Optional[str] = None) -> None:
		return self._execute_function("Page.generateTestReport", {"message": message, "group": group})
	
	def _get_ad_script_ancestry_impl(self, frame_id: str) -> Optional[Dict[str, Any]]:
		return self._execute_function("Page.getAdScriptAncestry", {"frame_id": frame_id})
	
	def _get_app_id_impl(self) -> Tuple[Optional[str], Optional[str]]:
		return self._execute_function("Page.getAppId", {})
	
	def _get_app_manifest_impl(self, manifest_id: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]], Optional[str], Optional[Dict[str, Any]], Dict[str, Any]]:
		return self._execute_function("Page.getAppManifest", {"manifest_id": manifest_id})
	
	def _get_frame_tree_impl(self) -> Dict[str, Any]:
		return self._execute_function("Page.getFrameTree", {})
	
	def _get_installability_errors_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Page.getInstallabilityErrors", {})
	
	def _get_layout_metrics_impl(self) -> Tuple[
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any]
	]:
		return self._execute_function("Page.getLayoutMetrics", {})
	
	def _get_manifest_icons_impl(self) -> Optional[str]:
		return self._execute_function("Page.getManifestIcons", {})
	
	def _get_navigation_history_impl(self) -> Tuple[int, List[Dict[str, Any]]]:
		return self._execute_function("Page.getNavigationHistory", {})
	
	def _get_origin_trials_impl(self, frame_id: str) -> List[Dict[str, Any]]:
		return self._execute_function("Page.getOriginTrials", {"frame_id": frame_id})
	
	def _get_permissions_policy_state_impl(self, frame_id: str) -> List[Dict[str, Any]]:
		return self._execute_function("Page.getPermissionsPolicyState", {"frame_id": frame_id})
	
	def _get_resource_content_impl(self, frame_id: str, url: str) -> Tuple[str, bool]:
		return self._execute_function("Page.getResourceContent", {"frame_id": frame_id, "url": url})
	
	def _get_resource_tree_impl(self) -> Dict[str, Any]:
		return self._execute_function("Page.getResourceTree", {})
	
	def _handle_java_script_dialog_impl(self, accept: bool, prompt_text: Optional[str] = None) -> None:
		return self._execute_function(
				"Page.handleJavaScriptDialog",
				{"accept": accept, "prompt_text": prompt_text}
		)
	
	def _navigate_impl(
			self,
			url: str,
			referrer: Optional[str] = None,
			transition_type: Optional[str] = None,
			frame_id: Optional[str] = None,
			referrer_policy: Optional[str] = None
	) -> Tuple[str, Optional[str], Optional[str], Optional[bool]]:
		return self._execute_function(
				"Page.navigate",
				{
					"url": url,
					"referrer": referrer,
					"transition_type": transition_type,
					"frame_id": frame_id,
					"referrer_policy": referrer_policy
				}
		)
	
	def _navigate_to_history_entry_impl(self, entry_id: int) -> None:
		return self._execute_function("Page.navigateToHistoryEntry", {"entry_id": entry_id})
	
	def _print_to_pdf_impl(
			self,
			landscape: Optional[bool] = None,
			display_header_footer: Optional[bool] = None,
			print_background: Optional[bool] = None,
			scale: Optional[float] = None,
			paper_width: Optional[float] = None,
			paper_height: Optional[float] = None,
			margin_top: Optional[float] = None,
			margin_bottom: Optional[float] = None,
			margin_left: Optional[float] = None,
			margin_right: Optional[float] = None,
			page_ranges: Optional[str] = None,
			header_template: Optional[str] = None,
			footer_template: Optional[str] = None,
			prefer_css_page_size: Optional[bool] = None,
			transfer_mode: Optional[str] = None,
			generate_tagged_pdf: Optional[bool] = None,
			generate_document_outline: Optional[bool] = None
	) -> Tuple[str, Optional[str]]:
		return self._execute_function(
				"Page.printToPDF",
				{
					"landscape": landscape,
					"display_header_footer": display_header_footer,
					"print_background": print_background,
					"scale": scale,
					"paper_width": paper_width,
					"paper_height": paper_height,
					"margin_top": margin_top,
					"margin_bottom": margin_bottom,
					"margin_left": margin_left,
					"margin_right": margin_right,
					"page_ranges": page_ranges,
					"header_template": header_template,
					"footer_template": footer_template,
					"prefer_css_page_size": prefer_css_page_size,
					"transfer_mode": transfer_mode,
					"generate_tagged_pdf": generate_tagged_pdf,
					"generate_document_outline": generate_document_outline
				}
		)
	
	def _produce_compilation_cache_impl(self, scripts: List[Dict[str, Any]]) -> None:
		return self._execute_function("Page.produceCompilationCache", {"scripts": scripts})
	
	def _reload_impl(
			self,
			ignore_cache: Optional[bool] = None,
			script_to_evaluate_on_load: Optional[str] = None,
			loader_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Page.reload",
				{
					"ignore_cache": ignore_cache,
					"script_to_evaluate_on_load": script_to_evaluate_on_load,
					"loader_id": loader_id
				}
		)
	
	def _remove_script_to_evaluate_on_load_impl(self, identifier: str) -> None:
		return self._execute_function("Page.removeScriptToEvaluateOnLoad", {"identifier": identifier})
	
	def _remove_script_to_evaluate_on_new_document_impl(self, identifier: str) -> None:
		return self._execute_function("Page.removeScriptToEvaluateOnNewDocument", {"identifier": identifier})
	
	def _reset_navigation_history_impl(self) -> None:
		return self._execute_function("Page.resetNavigationHistory", {})
	
	def _screencast_frame_ack_impl(self, session_id: int) -> None:
		return self._execute_function("Page.screencastFrameAck", {"session_id": session_id})
	
	def _search_in_resource_impl(
			self,
			frame_id: str,
			url: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Page.searchInResource",
				{
					"frame_id": frame_id,
					"url": url,
					"query": query,
					"case_sensitive": case_sensitive,
					"is_regex": is_regex
				}
		)
	
	def _set_ad_blocking_enabled_impl(self, enabled: bool) -> None:
		return self._execute_function("Page.setAdBlockingEnabled", {"enabled": enabled})
	
	def _set_bypass_csp_impl(self, enabled: bool) -> None:
		return self._execute_function("Page.setBypassCSP", {"enabled": enabled})
	
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
			viewport: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Page.setDeviceMetricsOverride",
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
					"viewport": viewport
				}
		)
	
	def _set_device_orientation_override_impl(self, alpha: float, beta: float, gamma: float) -> None:
		return self._execute_function(
				"Page.setDeviceOrientationOverride",
				{"alpha": alpha, "beta": beta, "gamma": gamma}
		)
	
	def _set_document_content_impl(self, frame_id: str, html: str) -> None:
		return self._execute_function("Page.setDocumentContent", {"frame_id": frame_id, "html": html})
	
	def _set_download_behavior_impl(self, behavior: str, download_path: Optional[str] = None) -> None:
		return self._execute_function(
				"Page.setDownloadBehavior",
				{"behavior": behavior, "download_path": download_path}
		)
	
	def _set_font_families_impl(
			self,
			font_families: Dict[str, Any],
			for_scripts: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._execute_function(
				"Page.setFontFamilies",
				{"font_families": font_families, "for_scripts": for_scripts}
		)
	
	def _set_font_sizes_impl(self, font_sizes: Dict[str, Any]) -> None:
		return self._execute_function("Page.setFontSizes", {"font_sizes": font_sizes})
	
	def _set_geolocation_override_impl(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None
	) -> None:
		return self._execute_function(
				"Page.setGeolocationOverride",
				{"latitude": latitude, "longitude": longitude, "accuracy": accuracy}
		)
	
	def _set_intercept_file_chooser_dialog_impl(self, enabled: bool, cancel: Optional[bool] = None) -> None:
		return self._execute_function(
				"Page.setInterceptFileChooserDialog",
				{"enabled": enabled, "cancel": cancel}
		)
	
	def _set_lifecycle_events_enabled_impl(self, enabled: bool) -> None:
		return self._execute_function("Page.setLifecycleEventsEnabled", {"enabled": enabled})
	
	def _set_prerendering_allowed_impl(self, is_allowed: bool) -> None:
		return self._execute_function("Page.setPrerenderingAllowed", {"is_allowed": is_allowed})
	
	def _set_rph_registration_mode_impl(self, mode: str) -> None:
		return self._execute_function("Page.setRPHRegistrationMode", {"mode": mode})
	
	def _set_spc_transaction_mode_impl(self, mode: str) -> None:
		return self._execute_function("Page.setSPCTransactionMode", {"mode": mode})
	
	def _set_touch_emulation_enabled_impl(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return self._execute_function(
				"Page.setTouchEmulationEnabled",
				{"enabled": enabled, "configuration": configuration}
		)
	
	def _set_web_lifecycle_state_impl(self, state: str) -> None:
		return self._execute_function("Page.setWebLifecycleState", {"state": state})
	
	def _start_screencast_impl(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			max_width: Optional[int] = None,
			max_height: Optional[int] = None,
			every_nth_frame: Optional[int] = None
	) -> None:
		return self._execute_function(
				"Page.startScreencast",
				{
					"format_": format_,
					"quality": quality,
					"max_width": max_width,
					"max_height": max_height,
					"every_nth_frame": every_nth_frame
				}
		)
	
	def _stop_loading_impl(self) -> None:
		return self._execute_function("Page.stopLoading", {})
	
	def _stop_screencast_impl(self) -> None:
		return self._execute_function("Page.stopScreencast", {})
	
	def _wait_for_debugger_impl(self) -> None:
		return self._execute_function("Page.waitForDebugger", {})
