from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedPwaCDPExecutor"]


class UnifiedPwaCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _change_app_user_settings_impl(
			self,
			manifest_id: str,
			link_capturing: Optional[bool] = None,
			display_mode: Optional[str] = None
	) -> None:
		return self._execute_function(
				"PWA.changeAppUserSettings",
				{
					"manifest_id": manifest_id,
					"link_capturing": link_capturing,
					"display_mode": display_mode
				}
		)
	
	def _get_os_app_state_impl(self, manifest_id: str) -> Tuple[int, List[Dict[str, Any]]]:
		return self._execute_function("PWA.getOsAppState", {"manifest_id": manifest_id})
	
	def _install_impl(self, manifest_id: str, install_url_or_bundle_url: Optional[str] = None) -> None:
		return self._execute_function(
				"PWA.install",
				{
					"manifest_id": manifest_id,
					"install_url_or_bundle_url": install_url_or_bundle_url
				}
		)
	
	def _launch_files_in_app_impl(self, manifest_id: str, files: List[str]) -> List[str]:
		return self._execute_function("PWA.launchFilesInApp", {"manifest_id": manifest_id, "files": files})
	
	def _launch_impl(self, manifest_id: str, url: Optional[str] = None) -> str:
		return self._execute_function("PWA.launch", {"manifest_id": manifest_id, "url": url})
	
	def _open_current_page_in_app_impl(self, manifest_id: str) -> None:
		return self._execute_function("PWA.openCurrentPageInApp", {"manifest_id": manifest_id})
	
	def _uninstall_impl(self, manifest_id: str) -> None:
		return self._execute_function("PWA.uninstall", {"manifest_id": manifest_id})
