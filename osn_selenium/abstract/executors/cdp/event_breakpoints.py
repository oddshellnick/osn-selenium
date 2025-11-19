from abc import ABC, abstractmethod


__all__ = ["AbstractEventBreakpointsCDPExecutor"]


class AbstractEventBreakpointsCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		...
	
	@abstractmethod
	def set_instrumentation_breakpoint(self, event_name: str) -> None:
		...
