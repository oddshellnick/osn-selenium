from typing import List
from abc import ABC, abstractmethod


__all__ = ["AbstractPerformanceTimelineCDPExecutor"]


class AbstractPerformanceTimelineCDPExecutor(ABC):
	@abstractmethod
	def enable(self, event_types: List[str]) -> None:
		...
