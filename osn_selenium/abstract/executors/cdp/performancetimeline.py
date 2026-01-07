from typing import Any, List
from abc import ABC, abstractmethod


class AbstractPerformanceTimelineCDPExecutor(ABC):
	@abstractmethod
	def enable(self, event_types: List[str]) -> None:
		...
