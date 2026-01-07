from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.tracing import (
	AbstractTracingCDPExecutor
)


class TracingCDPExecutor(AbstractTracingCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def end(self) -> None:
		return await self._execute_function("Tracing.end", locals())
	
	async def get_categories(self) -> List[str]:
		return await self._execute_function("Tracing.getCategories", locals())
	
	async def record_clock_sync_marker(self, sync_id: str) -> None:
		return await self._execute_function("Tracing.recordClockSyncMarker", locals())
	
	async def request_memory_dump(
			self,
			deterministic: Optional[bool] = None,
			level_of_detail: Optional[str] = None
	) -> Tuple[str, bool]:
		return await self._execute_function("Tracing.requestMemoryDump", locals())
	
	async def start(
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
		return await self._execute_function("Tracing.start", locals())
