from typing import Optional
from abc import ABC, abstractmethod


__all__ = ["AbstractCastCDPExecutor"]


class AbstractCastCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self, presentation_url: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_sink_to_use(self, sink_name: str) -> None:
		...
	
	@abstractmethod
	def start_desktop_mirroring(self, sink_name: str) -> None:
		...
	
	@abstractmethod
	def start_tab_mirroring(self, sink_name: str) -> None:
		...
	
	@abstractmethod
	def stop_casting(self, sink_name: str) -> None:
		...
