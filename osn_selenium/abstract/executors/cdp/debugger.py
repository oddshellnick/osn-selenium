from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractDebuggerCDPExecutor"]


class AbstractDebuggerCDPExecutor(ABC):
	@abstractmethod
	def continue_to_location(self, location: Dict[str, Any], target_call_frames: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def disassemble_wasm_module(self, script_id: str) -> Tuple[Optional[str], int, List[int], Dict[str, Any]]:
		...
	
	@abstractmethod
	def enable(self, max_scripts_cache_size: Optional[float] = None) -> str:
		...
	
	@abstractmethod
	def evaluate_on_call_frame(
			self,
			call_frame_id: str,
			expression: str,
			object_group: Optional[str] = None,
			include_command_line_api: Optional[bool] = None,
			silent: Optional[bool] = None,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			throw_on_side_effect: Optional[bool] = None,
			timeout: Optional[float] = None
	) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def get_possible_breakpoints(
			self,
			start: Dict[str, Any],
			end: Optional[Dict[str, Any]] = None,
			restrict_to_function: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_script_source(self, script_id: str) -> Tuple[str, Optional[str]]:
		...
	
	@abstractmethod
	def get_stack_trace(self, stack_trace_id: Dict[str, Any]) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_wasm_bytecode(self, script_id: str) -> str:
		...
	
	@abstractmethod
	def next_wasm_disassembly_chunk(self, stream_id: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def pause(self) -> None:
		...
	
	@abstractmethod
	def pause_on_async_call(self, parent_stack_trace_id: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def remove_breakpoint(self, breakpoint_id: str) -> None:
		...
	
	@abstractmethod
	def restart_frame(self, call_frame_id: str, mode: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def resume(self, terminate_on_resume: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def search_in_content(
			self,
			script_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_async_call_stack_depth(self, max_depth: int) -> None:
		...
	
	@abstractmethod
	def set_blackbox_execution_contexts(self, unique_ids: List[str]) -> None:
		...
	
	@abstractmethod
	def set_blackbox_patterns(self, patterns: List[str], skip_anonymous: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def set_blackboxed_ranges(self, script_id: str, positions: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_breakpoint(self, location: Dict[str, Any], condition: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_breakpoint_by_url(
			self,
			line_number: int,
			url: Optional[str] = None,
			url_regex: Optional[str] = None,
			script_hash: Optional[str] = None,
			column_number: Optional[int] = None,
			condition: Optional[str] = None
	) -> Tuple[str, List[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def set_breakpoint_on_function_call(self, object_id: str, condition: Optional[str] = None) -> str:
		...
	
	@abstractmethod
	def set_breakpoints_active(self, active: bool) -> None:
		...
	
	@abstractmethod
	def set_instrumentation_breakpoint(self, instrumentation: str) -> str:
		...
	
	@abstractmethod
	def set_pause_on_exceptions(self, state: str) -> None:
		...
	
	@abstractmethod
	def set_return_value(self, new_value: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def set_script_source(
			self,
			script_id: str,
			script_source: str,
			dry_run: Optional[bool] = None,
			allow_top_frame_editing: Optional[bool] = None
	) -> Tuple[
		Optional[List[Dict[str, Any]]],
		Optional[bool],
		Optional[Dict[str, Any]],
		Optional[Dict[str, Any]],
		str,
		Optional[Dict[str, Any]]
	]:
		...
	
	@abstractmethod
	def set_skip_all_pauses(self, skip: bool) -> None:
		...
	
	@abstractmethod
	def set_variable_value(
			self,
			scope_number: int,
			variable_name: str,
			new_value: Dict[str, Any],
			call_frame_id: str
	) -> None:
		...
	
	@abstractmethod
	def step_into(
			self,
			break_on_async_call: Optional[bool] = None,
			skip_list: Optional[List[Dict[str, Any]]] = None
	) -> None:
		...
	
	@abstractmethod
	def step_out(self) -> None:
		...
	
	@abstractmethod
	def step_over(self, skip_list: Optional[List[Dict[str, Any]]] = None) -> None:
		...
