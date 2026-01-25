from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedTracingCDPExecutor"]


class UnifiedTracingCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _end_impl(self) -> None:
		return self._execute_function("Tracing.end", {})
	
	def _get_categories_impl(self) -> List[str]:
		return self._execute_function("Tracing.getCategories", {})
	
	def _record_clock_sync_marker_impl(self, sync_id: str) -> None:
		return self._execute_function("Tracing.recordClockSyncMarker", {"sync_id": sync_id})
	
	def _request_memory_dump_impl(
			self,
			deterministic: Optional[bool] = None,
			level_of_detail: Optional[str] = None
	) -> Tuple[str, bool]:
		return self._execute_function(
				"Tracing.requestMemoryDump",
				{"deterministic": deterministic, "level_of_detail": level_of_detail}
		)
	
	def _start_impl(
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
		return self._execute_function(
				"Tracing.start",
				{
					"categories": categories,
					"options": options,
					"buffer_usage_reporting_interval": buffer_usage_reporting_interval,
					"transfer_mode": transfer_mode,
					"stream_format": stream_format,
					"stream_compression": stream_compression,
					"trace_config": trace_config,
					"perfetto_config": perfetto_config,
					"tracing_backend": tracing_backend
				}
		)
