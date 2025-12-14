from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class AbstractSystemInfoCDPExecutor(ABC):
	@abstractmethod
	def get_feature_state(self, feature_state: str) -> bool:
		...
	
	@abstractmethod
	def get_info(self) -> Tuple[List[Any]]:
		...
	
	@abstractmethod
	def get_process_info(self) -> List[Any]:
		...
