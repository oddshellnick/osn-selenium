from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.pwa import (
	UnifiedPwaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.pwa import (
	AbstractPwaCDPExecutor
)


__all__ = ["PwaCDPExecutor"]


class PwaCDPExecutor(UnifiedPwaCDPExecutor, AbstractPwaCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedPwaCDPExecutor.__init__(self, execute_function=execute_function)
	
	def change_app_user_settings(
			self,
			manifest_id: str,
			link_capturing: Optional[bool] = None,
			display_mode: Optional[str] = None
	) -> None:
		return self._change_app_user_settings_impl(
				manifest_id=manifest_id,
				link_capturing=link_capturing,
				display_mode=display_mode
		)
	
	def get_os_app_state(self, manifest_id: str) -> Tuple[int, List[Dict[str, Any]]]:
		return self._get_os_app_state_impl(manifest_id=manifest_id)
	
	def install(self, manifest_id: str, install_url_or_bundle_url: Optional[str] = None) -> None:
		return self._install_impl(
				manifest_id=manifest_id,
				install_url_or_bundle_url=install_url_or_bundle_url
		)
	
	def launch(self, manifest_id: str, url: Optional[str] = None) -> str:
		return self._launch_impl(manifest_id=manifest_id, url=url)
	
	def launch_files_in_app(self, manifest_id: str, files: List[str]) -> List[str]:
		return self._launch_files_in_app_impl(manifest_id=manifest_id, files=files)
	
	def open_current_page_in_app(self, manifest_id: str) -> None:
		return self._open_current_page_in_app_impl(manifest_id=manifest_id)
	
	def uninstall(self, manifest_id: str) -> None:
		return self._uninstall_impl(manifest_id=manifest_id)
