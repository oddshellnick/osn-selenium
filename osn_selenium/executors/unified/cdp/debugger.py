from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedDebuggerCDPExecutor"]


class UnifiedDebuggerCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _continue_to_location_impl(self, location: Dict[str, Any], target_call_frames: Optional[str] = None) -> None:
		return self._execute_function(
				"Debugger.continueToLocation",
				{"location": location, "target_call_frames": target_call_frames}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("Debugger.disable", {})
	
	def _disassemble_wasm_module_impl(self, script_id: str) -> Tuple[Optional[str], int, List[int], Dict[str, Any]]:
		return self._execute_function("Debugger.disassembleWasmModule", {"script_id": script_id})
	
	def _enable_impl(self, max_scripts_cache_size: Optional[float] = None) -> str:
		return self._execute_function("Debugger.enable", {"max_scripts_cache_size": max_scripts_cache_size})
	
	def _evaluate_on_call_frame_impl(
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
		return self._execute_function(
				"Debugger.evaluateOnCallFrame",
				{
					"call_frame_id": call_frame_id,
					"expression": expression,
					"object_group": object_group,
					"include_command_line_api": include_command_line_api,
					"silent": silent,
					"return_by_value": return_by_value,
					"generate_preview": generate_preview,
					"throw_on_side_effect": throw_on_side_effect,
					"timeout": timeout
				}
		)
	
	def _get_possible_breakpoints_impl(
			self,
			start: Dict[str, Any],
			end: Optional[Dict[str, Any]] = None,
			restrict_to_function: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Debugger.getPossibleBreakpoints",
				{
					"start": start,
					"end": end,
					"restrict_to_function": restrict_to_function
				}
		)
	
	def _get_script_source_impl(self, script_id: str) -> Tuple[str, Optional[str]]:
		return self._execute_function("Debugger.getScriptSource", {"script_id": script_id})
	
	def _get_stack_trace_impl(self, stack_trace_id: Dict[str, Any]) -> Dict[str, Any]:
		return self._execute_function("Debugger.getStackTrace", {"stack_trace_id": stack_trace_id})
	
	def _get_wasm_bytecode_impl(self, script_id: str) -> str:
		return self._execute_function("Debugger.getWasmBytecode", {"script_id": script_id})
	
	def _next_wasm_disassembly_chunk_impl(self, stream_id: str) -> Dict[str, Any]:
		return self._execute_function("Debugger.nextWasmDisassemblyChunk", {"stream_id": stream_id})
	
	def _pause_impl(self) -> None:
		return self._execute_function("Debugger.pause", {})
	
	def _pause_on_async_call_impl(self, parent_stack_trace_id: Dict[str, Any]) -> None:
		return self._execute_function(
				"Debugger.pauseOnAsyncCall",
				{"parent_stack_trace_id": parent_stack_trace_id}
		)
	
	def _remove_breakpoint_impl(self, breakpoint_id: str) -> None:
		return self._execute_function("Debugger.removeBreakpoint", {"breakpoint_id": breakpoint_id})
	
	def _restart_frame_impl(self, call_frame_id: str, mode: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
		return self._execute_function("Debugger.restartFrame", {"call_frame_id": call_frame_id, "mode": mode})
	
	def _resume_impl(self, terminate_on_resume: Optional[bool] = None) -> None:
		return self._execute_function("Debugger.resume", {"terminate_on_resume": terminate_on_resume})
	
	def _search_in_content_impl(
			self,
			script_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Debugger.searchInContent",
				{
					"script_id": script_id,
					"query": query,
					"case_sensitive": case_sensitive,
					"is_regex": is_regex
				}
		)
	
	def _set_async_call_stack_depth_impl(self, max_depth: int) -> None:
		return self._execute_function("Debugger.setAsyncCallStackDepth", {"max_depth": max_depth})
	
	def _set_blackbox_execution_contexts_impl(self, unique_ids: List[str]) -> None:
		return self._execute_function("Debugger.setBlackboxExecutionContexts", {"unique_ids": unique_ids})
	
	def _set_blackbox_patterns_impl(self, patterns: List[str], skip_anonymous: Optional[bool] = None) -> None:
		return self._execute_function(
				"Debugger.setBlackboxPatterns",
				{"patterns": patterns, "skip_anonymous": skip_anonymous}
		)
	
	def _set_blackboxed_ranges_impl(self, script_id: str, positions: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"Debugger.setBlackboxedRanges",
				{"script_id": script_id, "positions": positions}
		)
	
	def _set_breakpoint_by_url_impl(
			self,
			line_number: int,
			url: Optional[str] = None,
			url_regex: Optional[str] = None,
			script_hash: Optional[str] = None,
			column_number: Optional[int] = None,
			condition: Optional[str] = None
	) -> Tuple[str, List[Dict[str, Any]]]:
		return self._execute_function(
				"Debugger.setBreakpointByUrl",
				{
					"line_number": line_number,
					"url": url,
					"url_regex": url_regex,
					"script_hash": script_hash,
					"column_number": column_number,
					"condition": condition
				}
		)
	
	def _set_breakpoint_impl(self, location: Dict[str, Any], condition: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
		return self._execute_function("Debugger.setBreakpoint", {"location": location, "condition": condition})
	
	def _set_breakpoint_on_function_call_impl(self, object_id: str, condition: Optional[str] = None) -> str:
		return self._execute_function(
				"Debugger.setBreakpointOnFunctionCall",
				{"object_id": object_id, "condition": condition}
		)
	
	def _set_breakpoints_active_impl(self, active: bool) -> None:
		return self._execute_function("Debugger.setBreakpointsActive", {"active": active})
	
	def _set_instrumentation_breakpoint_impl(self, instrumentation: str) -> str:
		return self._execute_function(
				"Debugger.setInstrumentationBreakpoint",
				{"instrumentation": instrumentation}
		)
	
	def _set_pause_on_exceptions_impl(self, state: str) -> None:
		return self._execute_function("Debugger.setPauseOnExceptions", {"state": state})
	
	def _set_return_value_impl(self, new_value: Dict[str, Any]) -> None:
		return self._execute_function("Debugger.setReturnValue", {"new_value": new_value})
	
	def _set_script_source_impl(
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
		return self._execute_function(
				"Debugger.setScriptSource",
				{
					"script_id": script_id,
					"script_source": script_source,
					"dry_run": dry_run,
					"allow_top_frame_editing": allow_top_frame_editing
				}
		)
	
	def _set_skip_all_pauses_impl(self, skip: bool) -> None:
		return self._execute_function("Debugger.setSkipAllPauses", {"skip": skip})
	
	def _set_variable_value_impl(
			self,
			scope_number: int,
			variable_name: str,
			new_value: Dict[str, Any],
			call_frame_id: str
	) -> None:
		return self._execute_function(
				"Debugger.setVariableValue",
				{
					"scope_number": scope_number,
					"variable_name": variable_name,
					"new_value": new_value,
					"call_frame_id": call_frame_id
				}
		)
	
	def _step_into_impl(
			self,
			break_on_async_call: Optional[bool] = None,
			skip_list: Optional[List[Dict[str, Any]]] = None
	) -> None:
		return self._execute_function(
				"Debugger.stepInto",
				{"break_on_async_call": break_on_async_call, "skip_list": skip_list}
		)
	
	def _step_out_impl(self) -> None:
		return self._execute_function("Debugger.stepOut", {})
	
	def _step_over_impl(self, skip_list: Optional[List[Dict[str, Any]]] = None) -> None:
		return self._execute_function("Debugger.stepOver", {"skip_list": skip_list})
