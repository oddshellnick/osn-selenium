from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.browser import (
	UnifiedBrowserCDPExecutor
)
from osn_selenium.abstract.executors.cdp.browser import (
	AbstractBrowserCDPExecutor
)


__all__ = ["BrowserCDPExecutor"]


class BrowserCDPExecutor(UnifiedBrowserCDPExecutor, AbstractBrowserCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedBrowserCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_privacy_sandbox_coordinator_key_config(
			self,
			api: str,
			coordinator_origin: str,
			key_config: str,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._add_privacy_sandbox_coordinator_key_config_impl(
				api=api,
				coordinator_origin=coordinator_origin,
				key_config=key_config,
				browser_context_id=browser_context_id
		)
	
	def add_privacy_sandbox_enrollment_override(self, url: str) -> None:
		return self._add_privacy_sandbox_enrollment_override_impl(url=url)
	
	def cancel_download(self, guid: str, browser_context_id: Optional[str] = None) -> None:
		return self._cancel_download_impl(guid=guid, browser_context_id=browser_context_id)
	
	def close(self) -> None:
		return self._close_impl()
	
	def crash(self) -> None:
		return self._crash_impl()
	
	def crash_gpu_process(self) -> None:
		return self._crash_gpu_process_impl()
	
	def execute_browser_command(self, command_id: str) -> None:
		return self._execute_browser_command_impl(command_id=command_id)
	
	def get_browser_command_line(self) -> List[str]:
		return self._get_browser_command_line_impl()
	
	def get_histogram(self, name: str, delta: Optional[bool] = None) -> Dict[str, Any]:
		return self._get_histogram_impl(name=name, delta=delta)
	
	def get_histograms(self, query: Optional[str] = None, delta: Optional[bool] = None) -> List[Dict[str, Any]]:
		return self._get_histograms_impl(query=query, delta=delta)
	
	def get_version(self) -> Tuple[str, str, str, str, str]:
		return self._get_version_impl()
	
	def get_window_bounds(self, window_id: int) -> Dict[str, Any]:
		return self._get_window_bounds_impl(window_id=window_id)
	
	def get_window_for_target(self, target_id: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
		return self._get_window_for_target_impl(target_id=target_id)
	
	def grant_permissions(
			self,
			permissions: List[str],
			origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._grant_permissions_impl(
				permissions=permissions,
				origin=origin,
				browser_context_id=browser_context_id
		)
	
	def reset_permissions(self, browser_context_id: Optional[str] = None) -> None:
		return self._reset_permissions_impl(browser_context_id=browser_context_id)
	
	def set_contents_size(
			self,
			window_id: int,
			width: Optional[int] = None,
			height: Optional[int] = None
	) -> None:
		return self._set_contents_size_impl(window_id=window_id, width=width, height=height)
	
	def set_dock_tile(self, badge_label: Optional[str] = None, image: Optional[str] = None) -> None:
		return self._set_dock_tile_impl(badge_label=badge_label, image=image)
	
	def set_download_behavior(
			self,
			behavior: str,
			browser_context_id: Optional[str] = None,
			download_path: Optional[str] = None,
			events_enabled: Optional[bool] = None
	) -> None:
		return self._set_download_behavior_impl(
				behavior=behavior,
				browser_context_id=browser_context_id,
				download_path=download_path,
				events_enabled=events_enabled
		)
	
	def set_permission(
			self,
			permission: Dict[str, Any],
			setting: str,
			origin: Optional[str] = None,
			embedded_origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._set_permission_impl(
				permission=permission,
				setting=setting,
				origin=origin,
				embedded_origin=embedded_origin,
				browser_context_id=browser_context_id
		)
	
	def set_window_bounds(self, window_id: int, bounds: Dict[str, Any]) -> None:
		return self._set_window_bounds_impl(window_id=window_id, bounds=bounds)
