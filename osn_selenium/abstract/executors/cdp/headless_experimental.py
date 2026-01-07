from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


class AbstractHeadlessExperimentalCDPExecutor(ABC):
	@abstractmethod
	def begin_frame(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Any] = None
	) -> Tuple[bool, Optional[str]]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
