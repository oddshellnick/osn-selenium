from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedTargetCDPExecutor"]


class UnifiedTargetCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _activate_target_impl(self, target_id: str) -> None:
		return self._execute_function("Target.activateTarget", {"target_id": target_id})
	
	def _attach_to_browser_target_impl(self) -> str:
		return self._execute_function("Target.attachToBrowserTarget", {})
	
	def _attach_to_target_impl(self, target_id: str, flatten: Optional[bool] = None) -> str:
		return self._execute_function("Target.attachToTarget", {"target_id": target_id, "flatten": flatten})
	
	def _auto_attach_related_impl(
			self,
			target_id: str,
			wait_for_debugger_on_start: bool,
			filter_: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._execute_function(
				"Target.autoAttachRelated",
				{
					"target_id": target_id,
					"wait_for_debugger_on_start": wait_for_debugger_on_start,
					"filter_": filter_
				}
		)
	
	def _close_target_impl(self, target_id: str) -> bool:
		return self._execute_function("Target.closeTarget", {"target_id": target_id})
	
	def _create_browser_context_impl(
			self,
			dispose_on_detach: Optional[bool] = None,
			proxy_server: Optional[str] = None,
			proxy_bypass_list: Optional[str] = None,
			origins_with_universal_network_access: Optional[List[str]] = None
	) -> str:
		return self._execute_function(
				"Target.createBrowserContext",
				{
					"dispose_on_detach": dispose_on_detach,
					"proxy_server": proxy_server,
					"proxy_bypass_list": proxy_bypass_list,
					"origins_with_universal_network_access": origins_with_universal_network_access
				}
		)
	
	def _create_target_impl(
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
		return self._execute_function(
				"Target.createTarget",
				{
					"url": url,
					"left": left,
					"top": top,
					"width": width,
					"height": height,
					"window_state": window_state,
					"browser_context_id": browser_context_id,
					"enable_begin_frame_control": enable_begin_frame_control,
					"new_window": new_window,
					"background": background,
					"for_tab": for_tab,
					"hidden": hidden
				}
		)
	
	def _detach_from_target_impl(self, session_id: Optional[str] = None, target_id: Optional[str] = None) -> None:
		return self._execute_function(
				"Target.detachFromTarget",
				{"session_id": session_id, "target_id": target_id}
		)
	
	def _dispose_browser_context_impl(self, browser_context_id: str) -> None:
		return self._execute_function(
				"Target.disposeBrowserContext",
				{"browser_context_id": browser_context_id}
		)
	
	def _expose_dev_tools_protocol_impl(
			self,
			target_id: str,
			binding_name: Optional[str] = None,
			inherit_permissions: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Target.exposeDevToolsProtocol",
				{
					"target_id": target_id,
					"binding_name": binding_name,
					"inherit_permissions": inherit_permissions
				}
		)
	
	def _get_browser_contexts_impl(self) -> List[str]:
		return self._execute_function("Target.getBrowserContexts", {})
	
	def _get_target_info_impl(self, target_id: Optional[str] = None) -> Dict[str, Any]:
		return self._execute_function("Target.getTargetInfo", {"target_id": target_id})
	
	def _get_targets_impl(self, filter_: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
		return self._execute_function("Target.getTargets", {"filter_": filter_})
	
	def _open_dev_tools_impl(self, target_id: str) -> str:
		return self._execute_function("Target.openDevTools", {"target_id": target_id})
	
	def _send_message_to_target_impl(
			self,
			message: str,
			session_id: Optional[str] = None,
			target_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Target.sendMessageToTarget",
				{"message": message, "session_id": session_id, "target_id": target_id}
		)
	
	def _set_auto_attach_impl(
			self,
			auto_attach: bool,
			wait_for_debugger_on_start: bool,
			flatten: Optional[bool] = None,
			filter_: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._execute_function(
				"Target.setAutoAttach",
				{
					"auto_attach": auto_attach,
					"wait_for_debugger_on_start": wait_for_debugger_on_start,
					"flatten": flatten,
					"filter_": filter_
				}
		)
	
	def _set_discover_targets_impl(self, discover: bool, filter_: Optional[List[Dict[str, Any]]] = None) -> None:
		return self._execute_function("Target.setDiscoverTargets", {"discover": discover, "filter_": filter_})
	
	def _set_remote_locations_impl(self, locations: List[Dict[str, Any]]) -> None:
		return self._execute_function("Target.setRemoteLocations", {"locations": locations})
