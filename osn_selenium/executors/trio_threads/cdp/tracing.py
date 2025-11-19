import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.tracing import (
	UnifiedTracingCDPExecutor
)
from osn_selenium.abstract.executors.cdp.tracing import (
	AbstractTracingCDPExecutor
)


__all__ = ["TracingCDPExecutor"]


class TracingCDPExecutor(UnifiedTracingCDPExecutor, TrioThreadMixin, AbstractTracingCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedTracingCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def end(self) -> None:
		return await self.sync_to_trio(sync_function=self._end_impl)()
	
	async def get_categories(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_categories_impl)()
	
	async def record_clock_sync_marker(self, sync_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._record_clock_sync_marker_impl)(sync_id=sync_id)
	
	async def request_memory_dump(
			self,
			deterministic: Optional[bool] = None,
			level_of_detail: Optional[str] = None
	) -> Tuple[str, bool]:
		return await self.sync_to_trio(sync_function=self._request_memory_dump_impl)(deterministic=deterministic, level_of_detail=level_of_detail)
	
	async def start(
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
		return await self.sync_to_trio(sync_function=self._start_impl)(
				categories=categories,
				options=options,
				buffer_usage_reporting_interval=buffer_usage_reporting_interval,
				transfer_mode=transfer_mode,
				stream_format=stream_format,
				stream_compression=stream_compression,
				trace_config=trace_config,
				perfetto_config=perfetto_config,
				tracing_backend=tracing_backend
		)
