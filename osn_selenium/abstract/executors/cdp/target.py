from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractTargetCDPExecutor"]


class AbstractTargetCDPExecutor(ABC):
	@abstractmethod
	def activate_target(self, target_id: str) -> None:
		...
	
	@abstractmethod
	def attach_to_browser_target(self) -> str:
		...
	
	@abstractmethod
	def attach_to_target(self, target_id: str, flatten: Optional[bool] = None) -> str:
		...
	
	@abstractmethod
	def auto_attach_related(
			self,
			target_id: str,
			wait_for_debugger_on_start: bool,
			filter_: Optional[List[Dict[str, Any]]] = None
	) -> None:
		...
	
	@abstractmethod
	def close_target(self, target_id: str) -> bool:
		...
	
	@abstractmethod
	def create_browser_context(
			self,
			dispose_on_detach: Optional[bool] = None,
			proxy_server: Optional[str] = None,
			proxy_bypass_list: Optional[str] = None,
			origins_with_universal_network_access: Optional[List[str]] = None
	) -> str:
		...
	
	@abstractmethod
	def create_target(
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
		...
	
	@abstractmethod
	def detach_from_target(self, session_id: Optional[str] = None, target_id: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def dispose_browser_context(self, browser_context_id: str) -> None:
		...
	
	@abstractmethod
	def expose_dev_tools_protocol(
			self,
			target_id: str,
			binding_name: Optional[str] = None,
			inherit_permissions: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def get_browser_contexts(self) -> List[str]:
		...
	
	@abstractmethod
	def get_target_info(self, target_id: Optional[str] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_targets(self, filter_: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def open_dev_tools(self, target_id: str) -> str:
		...
	
	@abstractmethod
	def send_message_to_target(
			self,
			message: str,
			session_id: Optional[str] = None,
			target_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def set_auto_attach(
			self,
			auto_attach: bool,
			wait_for_debugger_on_start: bool,
			flatten: Optional[bool] = None,
			filter_: Optional[List[Dict[str, Any]]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_discover_targets(self, discover: bool, filter_: Optional[List[Dict[str, Any]]] = None) -> None:
		...
	
	@abstractmethod
	def set_remote_locations(self, locations: List[Dict[str, Any]]) -> None:
		...
