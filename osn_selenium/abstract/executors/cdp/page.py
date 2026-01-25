from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractPageCDPExecutor"]


class AbstractPageCDPExecutor(ABC):
	@abstractmethod
	def add_compilation_cache(self, url: str, data: str) -> None:
		...
	
	@abstractmethod
	def add_script_to_evaluate_on_load(self, script_source: str) -> str:
		...
	
	@abstractmethod
	def add_script_to_evaluate_on_new_document(
			self,
			source: str,
			world_name: Optional[str] = None,
			include_command_line_api: Optional[bool] = None,
			run_immediately: Optional[bool] = None
	) -> str:
		...
	
	@abstractmethod
	def bring_to_front(self) -> None:
		...
	
	@abstractmethod
	def capture_screenshot(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			clip: Optional[Dict[str, Any]] = None,
			from_surface: Optional[bool] = None,
			capture_beyond_viewport: Optional[bool] = None,
			optimize_for_speed: Optional[bool] = None
	) -> str:
		...
	
	@abstractmethod
	def capture_snapshot(self, format_: Optional[str] = None) -> str:
		...
	
	@abstractmethod
	def clear_compilation_cache(self) -> None:
		...
	
	@abstractmethod
	def clear_device_metrics_override(self) -> None:
		...
	
	@abstractmethod
	def clear_device_orientation_override(self) -> None:
		...
	
	@abstractmethod
	def clear_geolocation_override(self) -> None:
		...
	
	@abstractmethod
	def close(self) -> None:
		...
	
	@abstractmethod
	def crash(self) -> None:
		...
	
	@abstractmethod
	def create_isolated_world(
			self,
			frame_id: str,
			world_name: Optional[str] = None,
			grant_univeral_access: Optional[bool] = None
	) -> int:
		...
	
	@abstractmethod
	def delete_cookie(self, cookie_name: str, url: str) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self, enable_file_chooser_opened_event: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def generate_test_report(self, message: str, group: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def get_ad_script_ancestry(self, frame_id: str) -> Optional[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_app_id(self) -> Tuple[Optional[str], Optional[str]]:
		...
	
	@abstractmethod
	def get_app_manifest(self, manifest_id: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]], Optional[str], Optional[Dict[str, Any]], Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_frame_tree(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_installability_errors(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_layout_metrics(self) -> Tuple[
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any],
		Dict[str, Any]
	]:
		...
	
	@abstractmethod
	def get_manifest_icons(self) -> Optional[str]:
		...
	
	@abstractmethod
	def get_navigation_history(self) -> Tuple[int, List[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def get_origin_trials(self, frame_id: str) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_permissions_policy_state(self, frame_id: str) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_resource_content(self, frame_id: str, url: str) -> Tuple[str, bool]:
		...
	
	@abstractmethod
	def get_resource_tree(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def handle_java_script_dialog(self, accept: bool, prompt_text: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def navigate(
			self,
			url: str,
			referrer: Optional[str] = None,
			transition_type: Optional[str] = None,
			frame_id: Optional[str] = None,
			referrer_policy: Optional[str] = None
	) -> Tuple[str, Optional[str], Optional[str], Optional[bool]]:
		...
	
	@abstractmethod
	def navigate_to_history_entry(self, entry_id: int) -> None:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def produce_compilation_cache(self, scripts: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def reload(
			self,
			ignore_cache: Optional[bool] = None,
			script_to_evaluate_on_load: Optional[str] = None,
			loader_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def remove_script_to_evaluate_on_load(self, identifier: str) -> None:
		...
	
	@abstractmethod
	def remove_script_to_evaluate_on_new_document(self, identifier: str) -> None:
		...
	
	@abstractmethod
	def reset_navigation_history(self) -> None:
		...
	
	@abstractmethod
	def screencast_frame_ack(self, session_id: int) -> None:
		...
	
	@abstractmethod
	def search_in_resource(
			self,
			frame_id: str,
			url: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_ad_blocking_enabled(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_bypass_csp(self, enabled: bool) -> None:
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
			viewport: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		...
	
	@abstractmethod
	def set_document_content(self, frame_id: str, html: str) -> None:
		...
	
	@abstractmethod
	def set_download_behavior(self, behavior: str, download_path: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_font_families(
			self,
			font_families: Dict[str, Any],
			for_scripts: Optional[List[Dict[str, Any]]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_font_sizes(self, font_sizes: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def set_geolocation_override(
			self,
			latitude: Optional[float] = None,
			longitude: Optional[float] = None,
			accuracy: Optional[float] = None
	) -> None:
		...
	
	@abstractmethod
	def set_intercept_file_chooser_dialog(self, enabled: bool, cancel: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def set_lifecycle_events_enabled(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_prerendering_allowed(self, is_allowed: bool) -> None:
		...
	
	@abstractmethod
	def set_rph_registration_mode(self, mode: str) -> None:
		...
	
	@abstractmethod
	def set_spc_transaction_mode(self, mode: str) -> None:
		...
	
	@abstractmethod
	def set_touch_emulation_enabled(self, enabled: bool, configuration: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_web_lifecycle_state(self, state: str) -> None:
		...
	
	@abstractmethod
	def start_screencast(
			self,
			format_: Optional[str] = None,
			quality: Optional[int] = None,
			max_width: Optional[int] = None,
			max_height: Optional[int] = None,
			every_nth_frame: Optional[int] = None
	) -> None:
		...
	
	@abstractmethod
	def stop_loading(self) -> None:
		...
	
	@abstractmethod
	def stop_screencast(self) -> None:
		...
	
	@abstractmethod
	def wait_for_debugger(self) -> None:
		...
