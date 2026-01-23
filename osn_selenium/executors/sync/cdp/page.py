from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.page import (
	UnifiedPageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.page import (
	AbstractPageCDPExecutor
)


__all__ = ["PageCDPExecutor"]


class PageCDPExecutor(UnifiedPageCDPExecutor, AbstractPageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedPageCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_compilation_cache(self, url: str, data: str) -> None:
		return self._add_compilation_cache_impl(url=url, data=data)
	
	def add_script_to_evaluate_on_load(self, script_source: str) -> str:
		return self._add_script_to_evaluate_on_load_impl(script_source=script_source)
	
	def add_script_to_evaluate_on_new_document(
			self,
			source: str,
			world_name: Optional[str] = None,
			include_command_line_api: Optional[bool] = None,
			run_immediately: Optional[bool] = None
	) -> str:
		return self._add_script_to_evaluate_on_new_document_impl(
				source=source,
				world_name=world_name,
				include_command_line_api=include_command_line_api,
				run_immediately=run_immediately
		)
	
	def bring_to_front(self) -> None:
		return self._bring_to_front_impl()
	
	def capture_screenshot(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			clip: Optional[Dict[str, Any]] = None,
			from_surface: Optional[bool] = None,
			capture_beyond_viewport: Optional[bool] = None,
			optimize_for_speed: Optional[bool] = None
	) -> str:
		return self._capture_screenshot_impl(
				format_=format_,
				quality=quality,
				clip=clip,
				from_surface=from_surface,
				capture_beyond_viewport=capture_beyond_viewport,
				optimize_for_speed=optimize_for_speed
		)
	
	def capture_snapshot(self, format_: Optional[str] = None) -> str:
		return self._capture_snapshot_impl(format_=format_)
	
	def clear_compilation_cache(self) -> None:
		return self._clear_compilation_cache_impl()
	
	def clear_device_metrics_override(self) -> None:
		return self._clear_device_metrics_override_impl()
	
	def clear_device_orientation_override(self) -> None:
		return self._clear_device_orientation_override_impl()
	
	def clear_geolocation_override(self) -> None:
		return self._clear_geolocation_override_impl()
	
	def close(self) -> None:
		return self._close_impl()
	
	def crash(self) -> None:
		return self._crash_impl()
	
	def create_isolated_world(
			self,
			frame_id: str,
			world_name: Optional[str] = None,
			grant_univeral_access: Optional[bool] = None
	) -> int:
		return self._create_isolated_world_impl(
				frame_id=frame_id,
				world_name=world_name,
				grant_univeral_access=grant_univeral_access
		)
	
	def delete_cookie(self, cookie_name: str, url: str) -> None:
		return self._delete_cookie_impl(cookie_name=cookie_name, url=url)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self, enable_file_chooser_opened_event: Optional[bool] = None) -> None:
		return self._enable_impl(enable_file_chooser_opened_event=enable_file_chooser_opened_event)
	
	def generate_test_report(self, message: str, group: Optional[str] = None) -> None:
		return self._generate_test_report_impl(message=message, group=group)
	
	def get_ad_script_ancestry(self, frame_id: str) -> Optional[Dict[str, Any]]:
		return self._get_ad_script_ancestry_impl(frame_id=frame_id)
	
	def get_app_id(self) -> Tuple[Optional[str], Optional[str]]:
		return self._get_app_id_impl()
	
	def get_app_manifest(self, manifest_id: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]], Optional[str], Optional[Dict[str, Any]], Dict[str, Any]]:
		return self._get_app_manifest_impl(manifest_id=manifest_id)
	
	def get_frame_tree(self) -> Dict[str, Any]:
		return self._get_frame_tree_impl()
	
	def get_installability_errors(self) -> List[Dict[str, Any]]:
		return self._get_installability_errors_impl()
	
	def get_layout_metrics(self) -> Tuple[
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any]
	]:
		return self._get_layout_metrics_impl()
	
	def get_manifest_icons(self) -> Optional[str]:
		return self._get_manifest_icons_impl()
	
	def get_navigation_history(self) -> Tuple[int, List[Dict[str, Any]]]:
		return self._get_navigation_history_impl()
	
	def get_origin_trials(self, frame_id: str) -> List[Dict[str, Any]]:
		return self._get_origin_trials_impl(frame_id=frame_id)
	
	def get_permissions_policy_state(self, frame_id: str) -> List[Dict[str, Any]]:
		return self._get_permissions_policy_state_impl(frame_id=frame_id)
	
	def get_resource_content(self, frame_id: str, url: str) -> Tuple[str, bool]:
		return self._get_resource_content_impl(frame_id=frame_id, url=url)
	
	def get_resource_tree(self) -> Dict[str, Any]:
		return self._get_resource_tree_impl()
	
	def handle_java_script_dialog(self, accept: bool, prompt_text: Optional[str] = None) -> None:
		return self._handle_java_script_dialog_impl(accept=accept, prompt_text=prompt_text)
	
	def navigate(
			self,
			url: str,
			referrer: Optional[str] = None,
			transition_type: Optional[str] = None,
			frame_id: Optional[str] = None,
			referrer_policy: Optional[str] = None
	) -> Tuple[str, Optional[str], Optional[str], Optional[bool]]:
		return self._navigate_impl(
				url=url,
				referrer=referrer,
				transition_type=transition_type,
				frame_id=frame_id,
				referrer_policy=referrer_policy
		)
	
	def navigate_to_history_entry(self, entry_id: int) -> None:
		return self._navigate_to_history_entry_impl(entry_id=entry_id)
	
	def print_to_pdf(
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
		return self._print_to_pdf_impl(
				landscape=landscape,
				display_header_footer=display_header_footer,
				print_background=print_background,
				scale=scale,
				paper_width=paper_width,
				paper_height=paper_height,
				margin_top=margin_top,
				margin_bottom=margin_bottom,
				margin_left=margin_left,
				margin_right=margin_right,
				page_ranges=page_ranges,
				header_template=header_template,
				footer_template=footer_template,
				prefer_css_page_size=prefer_css_page_size,
				transfer_mode=transfer_mode,
				generate_tagged_pdf=generate_tagged_pdf,
				generate_document_outline=generate_document_outline
		)
	
	def produce_compilation_cache(self, scripts: List[Dict[str, Any]]) -> None:
		return self._produce_compilation_cache_impl(scripts=scripts)
	
	def reload(
			self,
			ignore_cache: Optional[bool] = None,
			script_to_evaluate_on_load: Optional[str] = None,
			loader_id: Optional[str] = None
	) -> None:
		return self._reload_impl(
				ignore_cache=ignore_cache,
				script_to_evaluate_on_load=script_to_evaluate_on_load,
				loader_id=loader_id
		)
	
	def remove_script_to_evaluate_on_load(self, identifier: str) -> None:
		return self._remove_script_to_evaluate_on_load_impl(identifier=identifier)
	
	def remove_script_to_evaluate_on_new_document(self, identifier: str) -> None:
		return self._remove_script_to_evaluate_on_new_document_impl(identifier=identifier)
	
	def reset_navigation_history(self) -> None:
		return self._reset_navigation_history_impl()
	
	def screencast_frame_ack(self, session_id: int) -> None:
		return self._screencast_frame_ack_impl(session_id=session_id)
	
	def search_in_resource(
			self,
			frame_id: str,
			url: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._search_in_resource_impl(
				frame_id=frame_id,
				url=url,
				query=query,
				case_sensitive=case_sensitive,
				is_regex=is_regex
		)
	
	def set_ad_blocking_enabled(self, enabled: bool) -> None:
		return self._set_ad_blocking_enabled_impl(enabled=enabled)
	
	def set_bypass_csp(self, enabled: bool) -> None:
		return self._set_bypass_csp_impl(enabled=enabled)
	
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
			viewport: Optional[Dict[str, Any]] = None
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
				viewport=viewport
		)
	
	def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		return self._set_device_orientation_override_impl(alpha=alpha, beta=beta, gamma=gamma)
	
	def set_document_content(self, frame_id: str, html: str) -> None:
		return self._set_document_content_impl(frame_id=frame_id, html=html)
	
	def set_download_behavior(self, behavior: str, download_path: Optional[str] = None) -> None:
		return self._set_download_behavior_impl(behavior=behavior, download_path=download_path)
	
	def set_font_families(
			self,
			font_families: Dict[str, Any],
			for_scripts: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._set_font_families_impl(font_families=font_families, for_scripts=for_scripts)
	
	def set_font_sizes(self, font_sizes: Dict[str, Any]) -> None:
		return self._set_font_sizes_impl(font_sizes=font_sizes)
	
	def set_geolocation_override(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None
	) -> None:
		return self._set_geolocation_override_impl(latitude=latitude, longitude=longitude, accuracy=accuracy)
	
	def set_intercept_file_chooser_dialog(self, enabled: bool, cancel: Optional[bool] = None) -> None:
		return self._set_intercept_file_chooser_dialog_impl(enabled=enabled, cancel=cancel)
	
	def set_lifecycle_events_enabled(self, enabled: bool) -> None:
		return self._set_lifecycle_events_enabled_impl(enabled=enabled)
	
	def set_prerendering_allowed(self, is_allowed: bool) -> None:
		return self._set_prerendering_allowed_impl(is_allowed=is_allowed)
	
	def set_rph_registration_mode(self, mode: str) -> None:
		return self._set_rph_registration_mode_impl(mode=mode)
	
	def set_spc_transaction_mode(self, mode: str) -> None:
		return self._set_spc_transaction_mode_impl(mode=mode)
	
	def set_touch_emulation_enabled(self, enabled: bool, configuration: Optional[str] = None) -> None:
		return self._set_touch_emulation_enabled_impl(enabled=enabled, configuration=configuration)
	
	def set_web_lifecycle_state(self, state: str) -> None:
		return self._set_web_lifecycle_state_impl(state=state)
	
	def start_screencast(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			max_width: Optional[int] = None,
			max_height: Optional[int] = None,
			every_nth_frame: Optional[int] = None
	) -> None:
		return self._start_screencast_impl(
				format_=format_,
				quality=quality,
				max_width=max_width,
				max_height=max_height,
				every_nth_frame=every_nth_frame
		)
	
	def stop_loading(self) -> None:
		return self._stop_loading_impl()
	
	def stop_screencast(self) -> None:
		return self._stop_screencast_impl()
	
	def wait_for_debugger(self) -> None:
		return self._wait_for_debugger_impl()
