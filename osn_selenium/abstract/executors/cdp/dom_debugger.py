from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractDomDebuggerCDPExecutor"]


class AbstractDomDebuggerCDPExecutor(ABC):
	@abstractmethod
	def get_event_listeners(
			self,
			object_id: str,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def remove_dom_breakpoint(self, node_id: int, type_: str) -> None:
		...
	
	@abstractmethod
	def remove_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		...
	
	@abstractmethod
	def remove_xhr_breakpoint(self, url: str) -> None:
		...
	
	@abstractmethod
	def set_break_on_csp_violation(self, violation_types: List[str]) -> None:
		...
	
	@abstractmethod
	def set_dom_breakpoint(self, node_id: int, type_: str) -> None:
		...
	
	@abstractmethod
	def set_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_instrumentation_breakpoint(self, event_name: str) -> None:
		...
	
	@abstractmethod
	def set_xhr_breakpoint(self, url: str) -> None:
		...
