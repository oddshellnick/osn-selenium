from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.browser import (
	AbstractBrowserCDPExecutor
)


class BrowserCDPExecutor(AbstractBrowserCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_privacy_sandbox_coordinator_key_config(
			self,
			api: str,
			coordinator_origin: str,
			key_config: str,
			browser_context_id: Optional[str] = None
	) -> None:
		return await self._execute_function("Browser.addPrivacySandboxCoordinatorKeyConfig", locals())
	
	async def add_privacy_sandbox_enrollment_override(self, url: str) -> None:
		return await self._execute_function("Browser.addPrivacySandboxEnrollmentOverride", locals())
	
	async def cancel_download(self, guid: str, browser_context_id: Optional[str] = None) -> None:
		return await self._execute_function("Browser.cancelDownload", locals())
	
	async def close(self) -> None:
		return await self._execute_function("Browser.close", locals())
	
	async def crash(self) -> None:
		return await self._execute_function("Browser.crash", locals())
	
	async def crash_gpu_process(self) -> None:
		return await self._execute_function("Browser.crashGpuProcess", locals())
	
	async def execute_browser_command(self, command_id: str) -> None:
		return await self._execute_function("Browser.executeBrowserCommand", locals())
	
	async def get_browser_command_line(self) -> List[str]:
		return await self._execute_function("Browser.getBrowserCommandLine", locals())
	
	async def get_histogram(self, name: str, delta: Optional[bool] = None) -> List[Any]:
		return await self._execute_function("Browser.getHistogram", locals())
	
	async def get_histograms(self, query: Optional[str] = None, delta: Optional[bool] = None) -> List[List[Any]]:
		return await self._execute_function("Browser.getHistograms", locals())
	
	async def get_version(self) -> Tuple[str]:
		return await self._execute_function("Browser.getVersion", locals())
	
	async def get_window_bounds(self, window_id: int) -> Any:
		return await self._execute_function("Browser.getWindowBounds", locals())
	
	async def get_window_for_target(self, target_id: Optional[str] = None) -> Tuple[int]:
		return await self._execute_function("Browser.getWindowForTarget", locals())
	
	async def grant_permissions(
			self,
			permissions: List[str],
			origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return await self._execute_function("Browser.grantPermissions", locals())
	
	async def reset_permissions(self, browser_context_id: Optional[str] = None) -> None:
		return await self._execute_function("Browser.resetPermissions", locals())
	
	async def set_contents_size(
			self,
			window_id: int,
			width: Optional[int] = None,
			height: Optional[int] = None
	) -> None:
		return await self._execute_function("Browser.setContentsSize", locals())
	
	async def set_dock_tile(self, badge_label: Optional[str] = None, image: Optional[str] = None) -> None:
		return await self._execute_function("Browser.setDockTile", locals())
	
	async def set_download_behavior(
			self,
			behavior: str,
			browser_context_id: Optional[str] = None,
			download_path: Optional[str] = None,
			events_enabled: Optional[bool] = None
	) -> None:
		return await self._execute_function("Browser.setDownloadBehavior", locals())
	
	async def set_permission(
			self,
			permission: Any,
			setting: str,
			origin: Optional[str] = None,
			embedded_origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		return await self._execute_function("Browser.setPermission", locals())
	
	async def set_window_bounds(self, window_id: int, bounds: Any) -> None:
		return await self._execute_function("Browser.setWindowBounds", locals())
