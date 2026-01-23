from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.executors.unified.cdp.heap_profiler import (
	UnifiedHeapProfilerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.heap_profiler import (
	AbstractHeapProfilerCDPExecutor
)


__all__ = ["HeapProfilerCDPExecutor"]


class HeapProfilerCDPExecutor(UnifiedHeapProfilerCDPExecutor, AbstractHeapProfilerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedHeapProfilerCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_inspected_heap_object(self, heap_object_id: str) -> None:
		return self._add_inspected_heap_object_impl(heap_object_id=heap_object_id)
	
	def collect_garbage(self) -> None:
		return self._collect_garbage_impl()
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_heap_object_id(self, object_id: str) -> str:
		return self._get_heap_object_id_impl(object_id=object_id)
	
	def get_object_by_heap_object_id(self, object_id: str, object_group: Optional[str] = None) -> Dict[str, Any]:
		return self._get_object_by_heap_object_id_impl(object_id=object_id, object_group=object_group)
	
	def get_sampling_profile(self) -> Dict[str, Any]:
		return self._get_sampling_profile_impl()
	
	def start_sampling(
			self,
			sampling_interval: Optional[float] = None,
			stack_depth: Optional[float] = None,
			include_objects_collected_by_major_gc: Optional[bool] = None,
			include_objects_collected_by_minor_gc: Optional[bool] = None
	) -> None:
		return self._start_sampling_impl(
				sampling_interval=sampling_interval,
				stack_depth=stack_depth,
				include_objects_collected_by_major_gc=include_objects_collected_by_major_gc,
				include_objects_collected_by_minor_gc=include_objects_collected_by_minor_gc
		)
	
	def start_tracking_heap_objects(self, track_allocations: Optional[bool] = None) -> None:
		return self._start_tracking_heap_objects_impl(track_allocations=track_allocations)
	
	def stop_sampling(self) -> Dict[str, Any]:
		return self._stop_sampling_impl()
	
	def stop_tracking_heap_objects(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return self._stop_tracking_heap_objects_impl(
				report_progress=report_progress,
				treat_global_objects_as_roots=treat_global_objects_as_roots,
				capture_numeric_value=capture_numeric_value,
				expose_internals=expose_internals
		)
	
	def take_heap_snapshot(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return self._take_heap_snapshot_impl(
				report_progress=report_progress,
				treat_global_objects_as_roots=treat_global_objects_as_roots,
				capture_numeric_value=capture_numeric_value,
				expose_internals=expose_internals
		)
