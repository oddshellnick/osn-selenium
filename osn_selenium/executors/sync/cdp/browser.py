from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.browser import (
	AbstractBrowserCDPExecutor
)


class BrowserCDPExecutor(AbstractBrowserCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def add_privacy_sandbox_coordinator_key_config(
			self,
			api: str,
			coordinator_origin: str,
			key_config: str,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function("Browser.addPrivacySandboxCoordinatorKeyConfig", locals())
	
	def add_privacy_sandbox_enrollment_override(self, url: str) -> None:
		return self._execute_function("Browser.addPrivacySandboxEnrollmentOverride", locals())
	
	def cancel_download(self, guid: str, browser_context_id: Optional[str] = None) -> None:
		return self._execute_function("Browser.cancelDownload", locals())
	
	def close(self) -> None:
		return self._execute_function("Browser.close", locals())
	
	def crash(self) -> None:
		return self._execute_function("Browser.crash", locals())
	
	def crash_gpu_process(self) -> None:
		return self._execute_function("Browser.crashGpuProcess", locals())
	
	def execute_browser_command(self, command_id: str) -> None:
		return self._execute_function("Browser.executeBrowserCommand", locals())
	
	def get_browser_command_line(self) -> List[str]:
		return self._execute_function("Browser.getBrowserCommandLine", locals())
	
	def get_histogram(self, name: str, delta: Optional[bool] = None) -> List[Any]:
		return self._execute_function("Browser.getHistogram", locals())
	
	def get_histograms(self, query: Optional[str] = None, delta: Optional[bool] = None) -> List[List[Any]]:
		return self._execute_function("Browser.getHistograms", locals())
	
	def get_version(self) -> Tuple[str]:
		return self._execute_function("Browser.getVersion", locals())
	
	def get_window_bounds(self, window_id: int) -> Any:
		return self._execute_function("Browser.getWindowBounds", locals())
	
	def get_window_for_target(self, target_id: Optional[str] = None) -> Tuple[int]:
		return self._execute_function("Browser.getWindowForTarget", locals())
	
	def grant_permissions(
			self,
			permissions: List[str],
			origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function("Browser.grantPermissions", locals())
	
	def reset_permissions(self, browser_context_id: Optional[str] = None) -> None:
		return self._execute_function("Browser.resetPermissions", locals())
	
	def set_contents_size(
			self,
			window_id: int,
			width: Optional[int] = None,
			height: Optional[int] = None
	) -> None:
		return self._execute_function("Browser.setContentsSize", locals())
	
	def set_dock_tile(self, badge_label: Optional[str] = None, image: Optional[str] = None) -> None:
		return self._execute_function("Browser.setDockTile", locals())
	
	def set_download_behavior(
			self,
			behavior: str,
			browser_context_id: Optional[str] = None,
			download_path: Optional[str] = None,
			events_enabled: Optional[bool] = None
	) -> None:
		return self._execute_function("Browser.setDownloadBehavior", locals())
	
	def set_permission(
			self,
			permission: Any,
			setting: str,
			origin: Optional[str] = None,
			embedded_origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function("Browser.setPermission", locals())
	
	def set_window_bounds(self, window_id: int, bounds: Any) -> None:
		return self._execute_function("Browser.setWindowBounds", locals())
