from typing import Any, Dict
from abc import ABC, abstractmethod


class AbstractWebAudioCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_realtime_data(self, context_id: str) -> Dict[str, Any]:
		...
