from osn_selenium.abstract.executors.cdp.pwa import (
	AbstractPwaCDPExecutor
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


class PwaCDPExecutor(AbstractPwaCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def change_app_user_settings(
			self,
			manifest_id: str,
			link_capturing: Optional[bool] = None,
			display_mode: Optional[str] = None
	) -> None:
		return await self._execute_function("PWA.changeAppUserSettings", locals())
	
	async def get_os_app_state(self, manifest_id: str) -> Tuple[int, List[Any]]:
		return await self._execute_function("PWA.getOsAppState", locals())
	
	async def install(self, manifest_id: str, install_url_or_bundle_url: Optional[str] = None) -> None:
		return await self._execute_function("PWA.install", locals())
	
	async def launch(self, manifest_id: str, url: Optional[str] = None) -> str:
		return await self._execute_function("PWA.launch", locals())
	
	async def launch_files_in_app(self, manifest_id: str, files: List[str]) -> List[str]:
		return await self._execute_function("PWA.launchFilesInApp", locals())
	
	async def open_current_page_in_app(self, manifest_id: str) -> None:
		return await self._execute_function("PWA.openCurrentPageInApp", locals())
	
	async def uninstall(self, manifest_id: str) -> None:
		return await self._execute_function("PWA.uninstall", locals())
