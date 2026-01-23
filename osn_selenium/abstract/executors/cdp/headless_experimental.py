from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	Optional,
	Tuple
)


__all__ = ["AbstractHeadlessExperimentalCDPExecutor"]


class AbstractHeadlessExperimentalCDPExecutor(ABC):
	@abstractmethod
	def begin_frame(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Dict[str, Any]] = None
	) -> Tuple[bool, Optional[str]]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
