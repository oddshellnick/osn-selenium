from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.debugger import (
	UnifiedDebuggerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.debugger import (
	AbstractDebuggerCDPExecutor
)


__all__ = ["DebuggerCDPExecutor"]


class DebuggerCDPExecutor(UnifiedDebuggerCDPExecutor, AbstractDebuggerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedDebuggerCDPExecutor.__init__(self, execute_function=execute_function)
	
	def continue_to_location(self, location: Dict[str, Any], target_call_frames: Optional[str] = None) -> None:
		return self._continue_to_location_impl(location=location, target_call_frames=target_call_frames)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def disassemble_wasm_module(self, script_id: str) -> Tuple[Optional[str], int, List[int], Dict[str, Any]]:
		return self._disassemble_wasm_module_impl(script_id=script_id)
	
	def enable(self, max_scripts_cache_size: Optional[float] = None) -> str:
		return self._enable_impl(max_scripts_cache_size=max_scripts_cache_size)
	
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
		return self._evaluate_on_call_frame_impl(
				call_frame_id=call_frame_id,
				expression=expression,
				object_group=object_group,
				include_command_line_api=include_command_line_api,
				silent=silent,
				return_by_value=return_by_value,
				generate_preview=generate_preview,
				throw_on_side_effect=throw_on_side_effect,
				timeout=timeout
		)
	
	def get_possible_breakpoints(
			self,
			start: Dict[str, Any],
			end: Optional[Dict[str, Any]] = None,
			restrict_to_function: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._get_possible_breakpoints_impl(start=start, end=end, restrict_to_function=restrict_to_function)
	
	def get_script_source(self, script_id: str) -> Tuple[str, Optional[str]]:
		return self._get_script_source_impl(script_id=script_id)
	
	def get_stack_trace(self, stack_trace_id: Dict[str, Any]) -> Dict[str, Any]:
		return self._get_stack_trace_impl(stack_trace_id=stack_trace_id)
	
	def get_wasm_bytecode(self, script_id: str) -> str:
		return self._get_wasm_bytecode_impl(script_id=script_id)
	
	def next_wasm_disassembly_chunk(self, stream_id: str) -> Dict[str, Any]:
		return self._next_wasm_disassembly_chunk_impl(stream_id=stream_id)
	
	def pause(self) -> None:
		return self._pause_impl()
	
	def pause_on_async_call(self, parent_stack_trace_id: Dict[str, Any]) -> None:
		return self._pause_on_async_call_impl(parent_stack_trace_id=parent_stack_trace_id)
	
	def remove_breakpoint(self, breakpoint_id: str) -> None:
		return self._remove_breakpoint_impl(breakpoint_id=breakpoint_id)
	
	def restart_frame(self, call_frame_id: str, mode: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
		return self._restart_frame_impl(call_frame_id=call_frame_id, mode=mode)
	
	def resume(self, terminate_on_resume: Optional[bool] = None) -> None:
		return self._resume_impl(terminate_on_resume=terminate_on_resume)
	
	def search_in_content(
			self,
			script_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._search_in_content_impl(
				script_id=script_id,
				query=query,
				case_sensitive=case_sensitive,
				is_regex=is_regex
		)
	
	def set_async_call_stack_depth(self, max_depth: int) -> None:
		return self._set_async_call_stack_depth_impl(max_depth=max_depth)
	
	def set_blackbox_execution_contexts(self, unique_ids: List[str]) -> None:
		return self._set_blackbox_execution_contexts_impl(unique_ids=unique_ids)
	
	def set_blackbox_patterns(self, patterns: List[str], skip_anonymous: Optional[bool] = None) -> None:
		return self._set_blackbox_patterns_impl(patterns=patterns, skip_anonymous=skip_anonymous)
	
	def set_blackboxed_ranges(self, script_id: str, positions: List[Dict[str, Any]]) -> None:
		return self._set_blackboxed_ranges_impl(script_id=script_id, positions=positions)
	
	def set_breakpoint(self, location: Dict[str, Any], condition: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
		return self._set_breakpoint_impl(location=location, condition=condition)
	
	def set_breakpoint_by_url(
			self,
			line_number: int,
			url: Optional[str] = None,
			url_regex: Optional[str] = None,
			script_hash: Optional[str] = None,
			column_number: Optional[int] = None,
			condition: Optional[str] = None
	) -> Tuple[str, List[Dict[str, Any]]]:
		return self._set_breakpoint_by_url_impl(
				line_number=line_number,
				url=url,
				url_regex=url_regex,
				script_hash=script_hash,
				column_number=column_number,
				condition=condition
		)
	
	def set_breakpoint_on_function_call(self, object_id: str, condition: Optional[str] = None) -> str:
		return self._set_breakpoint_on_function_call_impl(object_id=object_id, condition=condition)
	
	def set_breakpoints_active(self, active: bool) -> None:
		return self._set_breakpoints_active_impl(active=active)
	
	def set_instrumentation_breakpoint(self, instrumentation: str) -> str:
		return self._set_instrumentation_breakpoint_impl(instrumentation=instrumentation)
	
	def set_pause_on_exceptions(self, state: str) -> None:
		return self._set_pause_on_exceptions_impl(state=state)
	
	def set_return_value(self, new_value: Dict[str, Any]) -> None:
		return self._set_return_value_impl(new_value=new_value)
	
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
		return self._set_script_source_impl(
				script_id=script_id,
				script_source=script_source,
				dry_run=dry_run,
				allow_top_frame_editing=allow_top_frame_editing
		)
	
	def set_skip_all_pauses(self, skip: bool) -> None:
		return self._set_skip_all_pauses_impl(skip=skip)
	
	def set_variable_value(
			self,
			scope_number: int,
			variable_name: str,
			new_value: Dict[str, Any],
			call_frame_id: str
	) -> None:
		return self._set_variable_value_impl(
				scope_number=scope_number,
				variable_name=variable_name,
				new_value=new_value,
				call_frame_id=call_frame_id
		)
	
	def step_into(
			self,
			break_on_async_call: Optional[bool] = None,
			skip_list: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._step_into_impl(break_on_async_call=break_on_async_call, skip_list=skip_list)
	
	def step_out(self) -> None:
		return self._step_out_impl()
	
	def step_over(self, skip_list: Optional[List[Dict[str, Any]]] = None) -> None:
		return self._step_over_impl(skip_list=skip_list)
