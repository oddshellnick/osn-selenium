from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.tracing import (
	AbstractTracingCDPExecutor
)


class TracingCDPExecutor(AbstractTracingCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def end(self) -> None:
		return self._execute_function("Tracing.end", locals())
	
	def get_categories(self) -> List[str]:
		return self._execute_function("Tracing.getCategories", locals())
	
	def record_clock_sync_marker(self, sync_id: str) -> None:
		return self._execute_function("Tracing.recordClockSyncMarker", locals())
	
	def request_memory_dump(
			self,
			deterministic: Optional[bool] = None,
			level_of_detail: Optional[str] = None
	) -> Tuple[str]:
		return self._execute_function("Tracing.requestMemoryDump", locals())
	
	def start(
			self,
			categories: Optional[str] = None,
			options: Optional[str] = None,
			buffer_usage_reporting_interval: Optional[float] = None,
			transfer_mode: Optional[str] = None,
			stream_format: Optional[str] = None,
			stream_compression: Optional[str] = None,
			trace_config: Optional[Any] = None,
			perfetto_config: Optional[str] = None,
			tracing_backend: Optional[str] = None
	) -> None:
		return self._execute_function("Tracing.start", locals())
