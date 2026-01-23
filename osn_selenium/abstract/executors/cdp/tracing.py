from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractTracingCDPExecutor"]


class AbstractTracingCDPExecutor(ABC):
	@abstractmethod
	def end(self) -> None:
		...
	
	@abstractmethod
	def get_categories(self) -> List[str]:
		...
	
	@abstractmethod
	def record_clock_sync_marker(self, sync_id: str) -> None:
		...
	
	@abstractmethod
	def request_memory_dump(
			self,
			deterministic: Optional[bool] = None,
			level_of_detail: Optional[str] = None
	) -> Tuple[str, bool]:
		...
	
	@abstractmethod
	def start(
			self,
			categories: Optional[str] = None,
			options: Optional[str] = None,
			buffer_usage_reporting_interval: Optional[float] = None,
			transfer_mode: Optional[str] = None,
			stream_format: Optional[str] = None,
			stream_compression: Optional[str] = None,
			trace_config: Optional[Dict[str, Any]] = None,
			perfetto_config: Optional[str] = None,
			tracing_backend: Optional[str] = None
	) -> None:
		...
