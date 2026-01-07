from typing import Any
from abc import ABC, abstractmethod


class AbstractMediaCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
