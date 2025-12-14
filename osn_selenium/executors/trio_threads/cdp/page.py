from osn_selenium.abstract.executors.cdp.page import (
	AbstractPageCDPExecutor
)
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)


class PageCDPExecutor(AbstractPageCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_compilation_cache(self, url: str, data: str) -> None:
		return await self._execute_function("Page.addCompilationCache", locals())
	
	async def add_script_to_evaluate_on_load(self, script_source: str) -> str:
		return await self._execute_function("Page.addScriptToEvaluateOnLoad", locals())
	
	async def add_script_to_evaluate_on_new_document(
			self,
			source: str,
			world_name: Optional[str] = None,
			include_command_line_api: Optional[bool] = None,
			run_immediately: Optional[bool] = None
	) -> str:
		return await self._execute_function("Page.addScriptToEvaluateOnNewDocument", locals())
	
	async def bring_to_front(self) -> None:
		return await self._execute_function("Page.bringToFront", locals())
	
	async def capture_screenshot(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			clip: Optional[Any] = None,
			from_surface: Optional[bool] = None,
			capture_beyond_viewport: Optional[bool] = None,
			optimize_for_speed: Optional[bool] = None
	) -> str:
		return await self._execute_function("Page.captureScreenshot", locals())
	
	async def capture_snapshot(self, format_: Optional[str] = None) -> str:
		return await self._execute_function("Page.captureSnapshot", locals())
	
	async def clear_compilation_cache(self) -> None:
		return await self._execute_function("Page.clearCompilationCache", locals())
	
	async def clear_device_metrics_override(self) -> None:
		return await self._execute_function("Page.clearDeviceMetricsOverride", locals())
	
	async def clear_device_orientation_override(self) -> None:
		return await self._execute_function("Page.clearDeviceOrientationOverride", locals())
	
	async def clear_geolocation_override(self) -> None:
		return await self._execute_function("Page.clearGeolocationOverride", locals())
	
	async def close(self) -> None:
		return await self._execute_function("Page.close", locals())
	
	async def crash(self) -> None:
		return await self._execute_function("Page.crash", locals())
	
	async def create_isolated_world(
			self,
			frame_id: str,
			world_name: Optional[str] = None,
			grant_univeral_access: Optional[bool] = None
	) -> int:
		return await self._execute_function("Page.createIsolatedWorld", locals())
	
	async def delete_cookie(self, cookie_name: str, url: str) -> None:
		return await self._execute_function("Page.deleteCookie", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("Page.disable", locals())
	
	async def enable(self, enable_file_chooser_opened_event: Optional[bool] = None) -> None:
		return await self._execute_function("Page.enable", locals())
	
	async def generate_test_report(self, message: str, group: Optional[str] = None) -> None:
		return await self._execute_function("Page.generateTestReport", locals())
	
	async def get_ad_script_ancestry(self, frame_id: str) -> Optional[Any]:
		return await self._execute_function("Page.getAdScriptAncestry", locals())
	
	async def get_app_id(self) -> Tuple[Optional[str], Optional[str]]:
		return await self._execute_function("Page.getAppId", locals())
	
	async def get_app_manifest(self, manifest_id: Optional[str] = None) -> Tuple[str, List[Any], Optional[str], Optional[Any], Any]:
		return await self._execute_function("Page.getAppManifest", locals())
	
	async def get_frame_tree(self) -> Any:
		return await self._execute_function("Page.getFrameTree", locals())
	
	async def get_installability_errors(self) -> List[Any]:
		return await self._execute_function("Page.getInstallabilityErrors", locals())
	
	async def get_layout_metrics(self) -> Tuple[Any, Any, Any, Any, Any, Any]:
		return await self._execute_function("Page.getLayoutMetrics", locals())
	
	async def get_manifest_icons(self) -> Optional[str]:
		return await self._execute_function("Page.getManifestIcons", locals())
	
	async def get_navigation_history(self) -> Tuple[int, List[Any]]:
		return await self._execute_function("Page.getNavigationHistory", locals())
	
	async def get_origin_trials(self, frame_id: str) -> List[Any]:
		return await self._execute_function("Page.getOriginTrials", locals())
	
	async def get_permissions_policy_state(self, frame_id: str) -> List[Any]:
		return await self._execute_function("Page.getPermissionsPolicyState", locals())
	
	async def get_resource_content(self, frame_id: str, url: str) -> Tuple[str, bool]:
		return await self._execute_function("Page.getResourceContent", locals())
	
	async def get_resource_tree(self) -> Any:
		return await self._execute_function("Page.getResourceTree", locals())
	
	async def handle_java_script_dialog(self, accept: bool, prompt_text: Optional[str] = None) -> None:
		return await self._execute_function("Page.handleJavaScriptDialog", locals())
	
	async def navigate(
			self,
			url: str,
			referrer: Optional[str] = None,
			transition_type: Optional[str] = None,
			frame_id: Optional[str] = None,
			referrer_policy: Optional[str] = None
	) -> Tuple[str, Optional[str], Optional[str], Optional[bool]]:
		return await self._execute_function("Page.navigate", locals())
	
	async def navigate_to_history_entry(self, entry_id: int) -> None:
		return await self._execute_function("Page.navigateToHistoryEntry", locals())
	
	async def print_to_pdf(
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
		return await self._execute_function("Page.printToPDF", locals())
	
	async def produce_compilation_cache(self, scripts: List[Any]) -> None:
		return await self._execute_function("Page.produceCompilationCache", locals())
	
	async def reload(
			self,
			ignore_cache: Optional[bool] = None,
			script_to_evaluate_on_load: Optional[str] = None,
			loader_id: Optional[str] = None
	) -> None:
		return await self._execute_function("Page.reload", locals())
	
	async def remove_script_to_evaluate_on_load(self, identifier: str) -> None:
		return await self._execute_function("Page.removeScriptToEvaluateOnLoad", locals())
	
	async def remove_script_to_evaluate_on_new_document(self, identifier: str) -> None:
		return await self._execute_function("Page.removeScriptToEvaluateOnNewDocument", locals())
	
	async def reset_navigation_history(self) -> None:
		return await self._execute_function("Page.resetNavigationHistory", locals())
	
	async def screencast_frame_ack(self, session_id: int) -> None:
		return await self._execute_function("Page.screencastFrameAck", locals())
	
	async def search_in_resource(
			self,
			frame_id: str,
			url: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Any]:
		return await self._execute_function("Page.searchInResource", locals())
	
	async def set_ad_blocking_enabled(self, enabled: bool) -> None:
		return await self._execute_function("Page.setAdBlockingEnabled", locals())
	
	async def set_bypass_csp(self, enabled: bool) -> None:
		return await self._execute_function("Page.setBypassCSP", locals())
	
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
			viewport: Optional[Any] = None
	) -> None:
		return await self._execute_function("Page.setDeviceMetricsOverride", locals())
	
	async def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		return await self._execute_function("Page.setDeviceOrientationOverride", locals())
	
	async def set_document_content(self, frame_id: str, html: str) -> None:
		return await self._execute_function("Page.setDocumentContent", locals())
	
	async def set_download_behavior(self, behavior: str, download_path: Optional[str] = None) -> None:
		return await self._execute_function("Page.setDownloadBehavior", locals())
	
	async def set_font_families(self, font_families: Any, for_scripts: Optional[List[Any]] = None) -> None:
		return await self._execute_function("Page.setFontFamilies", locals())
	
	async def set_font_sizes(self, font_sizes: Any) -> None:
		return await self._execute_function("Page.setFontSizes", locals())
	
	async def set_geolocation_override(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None
	) -> None:
		return await self._execute_function("Page.setGeolocationOverride", locals())
	
	async def set_intercept_file_chooser_dialog(self, enabled: bool, cancel: Optional[bool] = None) -> None:
		return await self._execute_function("Page.setInterceptFileChooserDialog", locals())
	
	async def set_lifecycle_events_enabled(self, enabled: bool) -> None:
		return await self._execute_function("Page.setLifecycleEventsEnabled", locals())
	
	async def set_prerendering_allowed(self, is_allowed: bool) -> None:
		return await self._execute_function("Page.setPrerenderingAllowed", locals())
	
	async def set_rph_registration_mode(self, mode: str) -> None:
		return await self._execute_function("Page.setRPHRegistrationMode", locals())
	
	async def set_spc_transaction_mode(self, mode: str) -> None:
		return await self._execute_function("Page.setSPCTransactionMode", locals())
	
	async def set_touch_emulation_enabled(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return await self._execute_function("Page.setTouchEmulationEnabled", locals())
	
	async def set_web_lifecycle_state(self, state: str) -> None:
		return await self._execute_function("Page.setWebLifecycleState", locals())
	
	async def start_screencast(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			max_width: Optional[int] = None,
			max_height: Optional[int] = None,
			every_nth_frame: Optional[int] = None
	) -> None:
		return await self._execute_function("Page.startScreencast", locals())
	
	async def stop_loading(self) -> None:
		return await self._execute_function("Page.stopLoading", locals())
	
	async def stop_screencast(self) -> None:
		return await self._execute_function("Page.stopScreencast", locals())
	
	async def wait_for_debugger(self) -> None:
		return await self._execute_function("Page.waitForDebugger", locals())
