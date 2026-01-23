import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.target import (
	UnifiedTargetCDPExecutor
)
from osn_selenium.abstract.executors.cdp.target import (
	AbstractTargetCDPExecutor
)


__all__ = ["TargetCDPExecutor"]


class TargetCDPExecutor(UnifiedTargetCDPExecutor, TrioThreadMixin, AbstractTargetCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedTargetCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def activate_target(self, target_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._activate_target_impl)(target_id=target_id)
	
	async def attach_to_browser_target(self) -> str:
		return await self.sync_to_trio(sync_function=self._attach_to_browser_target_impl)()
	
	async def attach_to_target(self, target_id: str, flatten: Optional[bool] = None) -> str:
		return await self.sync_to_trio(sync_function=self._attach_to_target_impl)(target_id=target_id, flatten=flatten)
	
	async def auto_attach_related(
			self,
			target_id: str,
			wait_for_debugger_on_start: bool,
			filter_: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._auto_attach_related_impl)(
				target_id=target_id,
				wait_for_debugger_on_start=wait_for_debugger_on_start,
				filter_=filter_
		)
	
	async def close_target(self, target_id: str) -> bool:
		return await self.sync_to_trio(sync_function=self._close_target_impl)(target_id=target_id)
	
	async def create_browser_context(
			self,
			dispose_on_detach: Optional[bool] = None,
			proxy_server: Optional[str] = None,
			proxy_bypass_list: Optional[str] = None,
			origins_with_universal_network_access: Optional[List[str]] = None
	) -> str:
		return await self.sync_to_trio(sync_function=self._create_browser_context_impl)(
				dispose_on_detach=dispose_on_detach,
				proxy_server=proxy_server,
				proxy_bypass_list=proxy_bypass_list,
				origins_with_universal_network_access=origins_with_universal_network_access
		)
	
	async def create_target(
			self,
			url: str,
			left: Optional[int] = None,
			top: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
			window_state: Optional[str] = None,
			browser_context_id: Optional[str] = None,
			enable_begin_frame_control: Optional[bool] = None,
			new_window: Optional[bool] = None,
			background: Optional[bool] = None,
			for_tab: Optional[bool] = None,
			hidden: Optional[bool] = None
	) -> str:
		return await self.sync_to_trio(sync_function=self._create_target_impl)(
				url=url,
				left=left,
				top=top,
				width=width,
				height=height,
				window_state=window_state,
				browser_context_id=browser_context_id,
				enable_begin_frame_control=enable_begin_frame_control,
				new_window=new_window,
				background=background,
				for_tab=for_tab,
				hidden=hidden
		)
	
	async def detach_from_target(self, session_id: Optional[str] = None, target_id: Optional[str] = None) -> None:
		return await self.sync_to_trio(sync_function=self._detach_from_target_impl)(session_id=session_id, target_id=target_id)
	
	async def dispose_browser_context(self, browser_context_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._dispose_browser_context_impl)(browser_context_id=browser_context_id)
	
	async def expose_dev_tools_protocol(
			self,
			target_id: str,
			binding_name: Optional[str] = None,
			inherit_permissions: Optional[bool] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._expose_dev_tools_protocol_impl)(
				target_id=target_id,
				binding_name=binding_name,
				inherit_permissions=inherit_permissions
		)
	
	async def get_browser_contexts(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_browser_contexts_impl)()
	
	async def get_target_info(self, target_id: Optional[str] = None) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_target_info_impl)(target_id=target_id)
	
	async def get_targets(self, filter_: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_targets_impl)(filter_=filter_)
	
	async def open_dev_tools(self, target_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._open_dev_tools_impl)(target_id=target_id)
	
	async def send_message_to_target(
			self,
			message: str,
			session_id: Optional[str] = None,
			target_id: Optional[str] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._send_message_to_target_impl)(message=message, session_id=session_id, target_id=target_id)
	
	async def set_auto_attach(
			self,
			auto_attach: bool,
			wait_for_debugger_on_start: bool,
			flatten: Optional[bool] = None,
			filter_: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_auto_attach_impl)(
				auto_attach=auto_attach,
				wait_for_debugger_on_start=wait_for_debugger_on_start,
				flatten=flatten,
				filter_=filter_
		)
	
	async def set_discover_targets(self, discover: bool, filter_: Optional[List[Dict[str, Any]]] = None) -> None:
		return await self.sync_to_trio(sync_function=self._set_discover_targets_impl)(discover=discover, filter_=filter_)
	
	async def set_remote_locations(self, locations: List[Dict[str, Any]]) -> None:
		return await self.sync_to_trio(sync_function=self._set_remote_locations_impl)(locations=locations)
