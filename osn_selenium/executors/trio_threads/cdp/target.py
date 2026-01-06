from osn_selenium.abstract.executors.cdp import (
	AbstractTargetCDPExecutor
)
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Literal,
	Optional
)


class TargetCDPExecutor(AbstractTargetCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def activate_target(self, target_id: str) -> None:
		await self._execute_function("Target.activateTarget", locals())
	
	async def attach_to_browser_target(self) -> str:
		return await self._execute_function("Target.attachToBrowserTarget", locals())
	
	async def attach_to_target(self, target_id: str, flatten: Optional[bool] = None) -> str:
		return await self._execute_function("Target.attachToTarget", locals())
	
	async def close_target(self, target_id: str) -> bool:
		return await self._execute_function("Target.closeTarget", locals())
	
	async def create_browser_context(
			self,
			dispose_on_detach: Optional[bool] = None,
			proxy_server: Optional[str] = None,
			proxy_bypass_list: Optional[str] = None,
			origins_with_universal_network_access: Optional[List[str]] = None,
	) -> str:
		return await self._execute_function("Target.createBrowserContext", locals())
	
	async def create_target(
			self,
			url: str = "",
			left: Optional[int] = None,
			top: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
			window_state: Optional[Literal["normal", "minimized", "maximized", "fullscreen"]] = None,
			browser_context_id: Optional[str] = None,
			enable_begin_frame_control: Optional[bool] = None,
			new_window: Optional[bool] = None,
			background: Optional[bool] = None,
			for_tab: Optional[bool] = None,
			hidden: Optional[bool] = None,
	) -> str:
		return await self._execute_function("Target.createTarget", locals())
	
	async def detach_from_target(self, session_id: Optional[str] = None, target_id: Optional[str] = None) -> None:
		await self._execute_function("Target.detachFromTarget", locals())
	
	async def dispose_browser_context(self, browser_context_id: str) -> None:
		await self._execute_function("Target.disposeBrowserContext", locals())
	
	async def expose_dev_tools_protocol(
			self,
			target_id: str,
			binding_name: Optional[str] = None,
			inherit_permissions: Optional[bool] = None,
	) -> None:
		await self._execute_function("Target.exposeDevToolsProtocol", locals())
	
	async def get_browser_contexts(self) -> List[str]:
		return await self._execute_function("Target.getBrowserContexts", locals())
	
	async def get_target_info(self, target_id: Optional[str] = None) -> Any:
		return await self._execute_function("Target.getTargetInfo", locals())
	
	async def get_targets(self, filter_: Optional[List[Any]] = None) -> Any:
		return await self._execute_function("Target.getTargets", locals())
	
	async def send_message_to_target(
			self,
			message: str,
			session_id: Optional[str] = None,
			target_id: Optional[str] = None,
	) -> None:
		await self._execute_function("Target.sendMessageToTarget", locals())
