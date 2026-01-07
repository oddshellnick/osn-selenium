from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.heapprofiler import (
	AbstractHeapProfilerCDPExecutor
)


class AsyncHeapProfilerCDPExecutor(AbstractHeapProfilerCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_inspected_heap_object(self, heap_object_id: str) -> None:
		return await self._execute_function("HeapProfiler.addInspectedHeapObject", locals())
	
	async def collect_garbage(self) -> None:
		return await self._execute_function("HeapProfiler.collectGarbage", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("HeapProfiler.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("HeapProfiler.enable", locals())
	
	async def get_heap_object_id(self, object_id: str) -> str:
		return await self._execute_function("HeapProfiler.getHeapObjectId", locals())
	
	async def get_object_by_heap_object_id(self, object_id: str, object_group: Optional[str] = None) -> Any:
		return await self._execute_function("HeapProfiler.getObjectByHeapObjectId", locals())
	
	async def get_sampling_profile(self) -> List[Any]:
		return await self._execute_function("HeapProfiler.getSamplingProfile", locals())
	
	async def start_sampling(
			self,
			sampling_interval: Optional[float] = None,
			stack_depth: Optional[float] = None,
			include_objects_collected_by_major_gc: Optional[bool] = None,
			include_objects_collected_by_minor_gc: Optional[bool] = None
	) -> None:
		return await self._execute_function("HeapProfiler.startSampling", locals())
	
	async def start_tracking_heap_objects(self, track_allocations: Optional[bool] = None) -> None:
		return await self._execute_function("HeapProfiler.startTrackingHeapObjects", locals())
	
	async def stop_sampling(self) -> List[Any]:
		return await self._execute_function("HeapProfiler.stopSampling", locals())
	
	async def stop_tracking_heap_objects(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return await self._execute_function("HeapProfiler.stopTrackingHeapObjects", locals())
	
	async def take_heap_snapshot(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		return await self._execute_function("HeapProfiler.takeHeapSnapshot", locals())
