from typing import Any
from abc import ABC, abstractmethod


class AbstractTetheringCDPExecutor(ABC):
	@abstractmethod
	def bind(self, port: int) -> None:
		...
	
	@abstractmethod
	def unbind(self, port: int) -> None:
		...
