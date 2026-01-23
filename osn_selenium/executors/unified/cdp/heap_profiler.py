from typing import (
	Any,
	Callable,
	Dict,
	Optional
)


__all__ = ["UnifiedHeapProfilerCDPExecutor"]


class UnifiedHeapProfilerCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_inspected_heap_object_impl(self, heap_object_id: str) -> None:
		return self._execute_function(
				"HeapProfiler.addInspectedHeapObject",
				{"heap_object_id": heap_object_id}
		)
	
	def _collect_garbage_impl(self) -> None:
		return self._execute_function("HeapProfiler.collectGarbage", {})
	
	def _disable_impl(self) -> None:
		return self._execute_function("HeapProfiler.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("HeapProfiler.enable", {})
	
	def _get_heap_object_id_impl(self, object_id: str) -> str:
		return self._execute_function("HeapProfiler.getHeapObjectId", {"object_id": object_id})
	
	def _get_object_by_heap_object_id_impl(self, object_id: str, object_group: Optional[str] = None) -> Dict[str, Any]:
		return self._execute_function(
				"HeapProfiler.getObjectByHeapObjectId",
				{"object_id": object_id, "object_group": object_group}
		)
	
	def _get_sampling_profile_impl(self) -> Dict[str, Any]:
		return self._execute_function("HeapProfiler.getSamplingProfile", {})
	
	def _start_sampling_impl(
			self,
			sampling_interval: Optional[float] = None,
			stack_depth: Optional[float] = None,
			include_objects_collected_by_major_gc: Optional[bool] = None,
			include_objects_collected_by_minor_gc: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"HeapProfiler.startSampling",
				{
					"sampling_interval": sampling_interval,
					"stack_depth": stack_depth,
					"include_objects_collected_by_major_gc": include_objects_collected_by_major_gc,
					"include_objects_collected_by_minor_gc": include_objects_collected_by_minor_gc
				}
		)
	
	def _start_tracking_heap_objects_impl(self, track_allocations: Optional[bool] = None) -> None:
		return self._execute_function(
				"HeapProfiler.startTrackingHeapObjects",
				{"track_allocations": track_allocations}
		)
	
	def _stop_sampling_impl(self) -> Dict[str, Any]:
		return self._execute_function("HeapProfiler.stopSampling", {})
	
	def _stop_tracking_heap_objects_impl(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"HeapProfiler.stopTrackingHeapObjects",
				{
					"report_progress": report_progress,
					"treat_global_objects_as_roots": treat_global_objects_as_roots,
					"capture_numeric_value": capture_numeric_value,
					"expose_internals": expose_internals
				}
		)
	
	def _take_heap_snapshot_impl(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"HeapProfiler.takeHeapSnapshot",
				{
					"report_progress": report_progress,
					"treat_global_objects_as_roots": treat_global_objects_as_roots,
					"capture_numeric_value": capture_numeric_value,
					"expose_internals": expose_internals
				}
		)
