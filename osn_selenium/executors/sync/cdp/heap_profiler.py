from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.abstract.executors.cdp.heap_profiler import (
	AbstractHeapProfilerCDPExecutor
)


class HeapProfilerCDPExecutor(AbstractHeapProfilerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def add_inspected_heap_object(self, heap_object_id: str) -> None:
		return self._execute_function("HeapProfiler.addInspectedHeapObject", locals())
	
	def collect_garbage(self) -> None:
		return self._execute_function("HeapProfiler.collectGarbage", locals())
	
	def disable(self) -> None:
		return self._execute_function("HeapProfiler.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("HeapProfiler.enable", locals())
	
	def get_heap_object_id(self, object_id: str) -> str:
		return self._execute_function("HeapProfiler.getHeapObjectId", locals())
	
	def get_object_by_heap_object_id(self, object_id: str, object_group: Optional[str] = None) -> Any:
		return self._execute_function("HeapProfiler.getObjectByHeapObjectId", locals())
	
	def get_sampling_profile(self) -> Any:
		return self._execute_function("HeapProfiler.getSamplingProfile", locals())
	
	def start_sampling(
			self,
			sampling_interval: Optional[float] = None,
			stack_depth: Optional[float] = None,
			include_objects_collected_by_major_gc: Optional[bool] = None,
			include_objects_collected_by_minor_gc: Optional[bool] = None
	) -> None:
		return self._execute_function("HeapProfiler.startSampling", locals())
	
	def start_tracking_heap_objects(self, track_allocations: Optional[bool] = None) -> None:
		return self._execute_function("HeapProfiler.startTrackingHeapObjects", locals())
	
	def stop_sampling(self) -> Any:
		return self._execute_function("HeapProfiler.stopSampling", locals())
	
	def stop_tracking_heap_objects(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return self._execute_function("HeapProfiler.stopTrackingHeapObjects", locals())
	
	def take_heap_snapshot(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return self._execute_function("HeapProfiler.takeHeapSnapshot", locals())
