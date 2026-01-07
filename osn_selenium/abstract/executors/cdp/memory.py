from abc import ABC, abstractmethod
from typing import (
	Any,
	List,
	Optional,
	Tuple
)


class AbstractMemoryCDPExecutor(ABC):
	@abstractmethod
	def forcibly_purge_java_script_memory(self) -> None:
		...
	
	@abstractmethod
	def get_all_time_sampling_profile(self) -> Any:
		...
	
	@abstractmethod
	def get_browser_sampling_profile(self) -> Any:
		...
	
	@abstractmethod
	def get_dom_counters(self) -> Tuple[int, int, int]:
		...
	
	@abstractmethod
	def get_dom_counters_for_leak_detection(self) -> List[Any]:
		...
	
	@abstractmethod
	def get_sampling_profile(self) -> Any:
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
