from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedBrowserCDPExecutor"]


class UnifiedBrowserCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_privacy_sandbox_coordinator_key_config_impl(
			self,
			api: str,
			coordinator_origin: str,
			key_config: str,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Browser.addPrivacySandboxCoordinatorKeyConfig",
				{
					"api": api,
					"coordinator_origin": coordinator_origin,
					"key_config": key_config,
					"browser_context_id": browser_context_id
				}
		)
	
	def _add_privacy_sandbox_enrollment_override_impl(self, url: str) -> None:
		return self._execute_function("Browser.addPrivacySandboxEnrollmentOverride", {"url": url})
	
	def _cancel_download_impl(self, guid: str, browser_context_id: Optional[str] = None) -> None:
		return self._execute_function(
				"Browser.cancelDownload",
				{"guid": guid, "browser_context_id": browser_context_id}
		)
	
	def _close_impl(self) -> None:
		return self._execute_function("Browser.close", {})
	
	def _crash_gpu_process_impl(self) -> None:
		return self._execute_function("Browser.crashGpuProcess", {})
	
	def _crash_impl(self) -> None:
		return self._execute_function("Browser.crash", {})
	
	def _execute_browser_command_impl(self, command_id: str) -> None:
		return self._execute_function("Browser.executeBrowserCommand", {"command_id": command_id})
	
	def _get_browser_command_line_impl(self) -> List[str]:
		return self._execute_function("Browser.getBrowserCommandLine", {})
	
	def _get_histogram_impl(self, name: str, delta: Optional[bool] = None) -> Dict[str, Any]:
		return self._execute_function("Browser.getHistogram", {"name": name, "delta": delta})
	
	def _get_histograms_impl(self, query: Optional[str] = None, delta: Optional[bool] = None) -> List[Dict[str, Any]]:
		return self._execute_function("Browser.getHistograms", {"query": query, "delta": delta})
	
	def _get_version_impl(self) -> Tuple[str, str, str, str, str]:
		return self._execute_function("Browser.getVersion", {})
	
	def _get_window_bounds_impl(self, window_id: int) -> Dict[str, Any]:
		return self._execute_function("Browser.getWindowBounds", {"window_id": window_id})
	
	def _get_window_for_target_impl(self, target_id: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
		return self._execute_function("Browser.getWindowForTarget", {"target_id": target_id})
	
	def _grant_permissions_impl(
			self,
			permissions: List[str],
			origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Browser.grantPermissions",
				{
					"permissions": permissions,
					"origin": origin,
					"browser_context_id": browser_context_id
				}
		)
	
	def _reset_permissions_impl(self, browser_context_id: Optional[str] = None) -> None:
		return self._execute_function("Browser.resetPermissions", {"browser_context_id": browser_context_id})
	
	def _set_contents_size_impl(
			self,
			window_id: int,
			width: Optional[int] = None,
			height: Optional[int] = None
	) -> None:
		return self._execute_function(
				"Browser.setContentsSize",
				{"window_id": window_id, "width": width, "height": height}
		)
	
	def _set_dock_tile_impl(self, badge_label: Optional[str] = None, image: Optional[str] = None) -> None:
		return self._execute_function("Browser.setDockTile", {"badge_label": badge_label, "image": image})
	
	def _set_download_behavior_impl(
			self,
			behavior: str,
			browser_context_id: Optional[str] = None,
			download_path: Optional[str] = None,
			events_enabled: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Browser.setDownloadBehavior",
				{
					"behavior": behavior,
					"browser_context_id": browser_context_id,
					"download_path": download_path,
					"events_enabled": events_enabled
				}
		)
	
	def _set_permission_impl(
			self,
			permission: Dict[str, Any],
			setting: str,
			origin: Optional[str] = None,
			embedded_origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Browser.setPermission",
				{
					"permission": permission,
					"setting": setting,
					"origin": origin,
					"embedded_origin": embedded_origin,
					"browser_context_id": browser_context_id
				}
		)
	
	def _set_window_bounds_impl(self, window_id: int, bounds: Dict[str, Any]) -> None:
		return self._execute_function("Browser.setWindowBounds", {"window_id": window_id, "bounds": bounds})
