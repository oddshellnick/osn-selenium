from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


__all__ = ["AbstractHeapProfilerCDPExecutor"]


class AbstractHeapProfilerCDPExecutor(ABC):
	@abstractmethod
	def add_inspected_heap_object(self, heap_object_id: str) -> None:
		...
	
	@abstractmethod
	def collect_garbage(self) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_heap_object_id(self, object_id: str) -> str:
		...
	
	@abstractmethod
	def get_object_by_heap_object_id(self, object_id: str, object_group: Optional[str] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_sampling_profile(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def start_sampling(
			self,
			sampling_interval: Optional[float] = None,
			stack_depth: Optional[float] = None,
			include_objects_collected_by_major_gc: Optional[bool] = None,
			include_objects_collected_by_minor_gc: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def start_tracking_heap_objects(self, track_allocations: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def stop_sampling(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def stop_tracking_heap_objects(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def take_heap_snapshot(
			self,
			report_progress: Optional[bool] = None,
			treat_global_objects_as_roots: Optional[bool] = None,
			capture_numeric_value: Optional[bool] = None,
			expose_internals: Optional[bool] = None
	) -> None:
		...
