from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractMemoryCDPExecutor"]


class AbstractMemoryCDPExecutor(ABC):
	@abstractmethod
	def forcibly_purge_java_script_memory(self) -> None:
		...
	
	@abstractmethod
	def get_all_time_sampling_profile(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_browser_sampling_profile(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_dom_counters(self) -> Tuple[int, int, int]:
		...
	
	@abstractmethod
	def get_dom_counters_for_leak_detection(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_sampling_profile(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def prepare_for_leak_detection(self) -> None:
		...
	
	@abstractmethod
	def set_pressure_notifications_suppressed(self, suppressed: bool) -> None:
		...
	
	@abstractmethod
	def simulate_pressure_notification(self, level: str) -> None:
		...
	
	@abstractmethod
	def start_sampling(
			self,
			sampling_interval: Optional[int] = None,
			suppress_randomness: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def stop_sampling(self) -> None:
		...
