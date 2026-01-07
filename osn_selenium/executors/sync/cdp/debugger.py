from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.debugger import (
	AbstractDebuggerCDPExecutor
)


class DebuggerCDPExecutor(AbstractDebuggerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def continue_to_location(self, location: Any, target_call_frames: Optional[str] = None) -> None:
		return self._execute_function("Debugger.continueToLocation", locals())
	
	def disable(self) -> None:
		return self._execute_function("Debugger.disable", locals())
	
	def disassemble_wasm_module(self, script_id: str) -> Tuple[Optional[str]]:
		return self._execute_function("Debugger.disassembleWasmModule", locals())
	
	def enable(self, max_scripts_cache_size: Optional[float] = None) -> str:
		return self._execute_function("Debugger.enable", locals())
	
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
	) -> Tuple[Any]:
		return self._execute_function("Debugger.evaluateOnCallFrame", locals())
	
	def get_possible_breakpoints(
			self,
			start: Any,
			end: Optional[Any] = None,
			restrict_to_function: Optional[bool] = None
	) -> List[Any]:
		return self._execute_function("Debugger.getPossibleBreakpoints", locals())
	
	def get_script_source(self, script_id: str) -> Tuple[str]:
		return self._execute_function("Debugger.getScriptSource", locals())
	
	def get_stack_trace(self, stack_trace_id: Any) -> List[Any]:
		return self._execute_function("Debugger.getStackTrace", locals())
	
	def get_wasm_bytecode(self, script_id: str) -> str:
		return self._execute_function("Debugger.getWasmBytecode", locals())
	
	def next_wasm_disassembly_chunk(self, stream_id: str) -> List[Any]:
		return self._execute_function("Debugger.nextWasmDisassemblyChunk", locals())
	
	def pause(self) -> None:
		return self._execute_function("Debugger.pause", locals())
	
	def pause_on_async_call(self, parent_stack_trace_id: Any) -> None:
		return self._execute_function("Debugger.pauseOnAsyncCall", locals())
	
	def remove_breakpoint(self, breakpoint_id: str) -> None:
		return self._execute_function("Debugger.removeBreakpoint", locals())
	
	def restart_frame(self, call_frame_id: str, mode: Optional[str] = None) -> Tuple[List[Any]]:
		return self._execute_function("Debugger.restartFrame", locals())
	
	def resume(self, terminate_on_resume: Optional[bool] = None) -> None:
		return self._execute_function("Debugger.resume", locals())
	
	def search_in_content(
			self,
			script_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Any]:
		return self._execute_function("Debugger.searchInContent", locals())
	
	def set_async_call_stack_depth(self, max_depth: int) -> None:
		return self._execute_function("Debugger.setAsyncCallStackDepth", locals())
	
	def set_blackbox_execution_contexts(self, unique_ids: List[str]) -> None:
		return self._execute_function("Debugger.setBlackboxExecutionContexts", locals())
	
	def set_blackbox_patterns(self, patterns: List[str], skip_anonymous: Optional[bool] = None) -> None:
		return self._execute_function("Debugger.setBlackboxPatterns", locals())
	
	def set_blackboxed_ranges(self, script_id: str, positions: List[Any]) -> None:
		return self._execute_function("Debugger.setBlackboxedRanges", locals())
	
	def set_breakpoint(self, location: Any, condition: Optional[str] = None) -> Tuple[str]:
		return self._execute_function("Debugger.setBreakpoint", locals())
	
	def set_breakpoint_by_url(
			self,
			line_number: int,
			url: Optional[str] = None,
			url_regex: Optional[str] = None,
			script_hash: Optional[str] = None,
			column_number: Optional[int] = None,
			condition: Optional[str] = None
	) -> Tuple[str]:
		return self._execute_function("Debugger.setBreakpointByUrl", locals())
	
	def set_breakpoint_on_function_call(self, object_id: str, condition: Optional[str] = None) -> str:
		return self._execute_function("Debugger.setBreakpointOnFunctionCall", locals())
	
	def set_breakpoints_active(self, active: bool) -> None:
		return self._execute_function("Debugger.setBreakpointsActive", locals())
	
	def set_instrumentation_breakpoint(self, instrumentation: str) -> str:
		return self._execute_function("Debugger.setInstrumentationBreakpoint", locals())
	
	def set_pause_on_exceptions(self, state: str) -> None:
		return self._execute_function("Debugger.setPauseOnExceptions", locals())
	
	def set_return_value(self, new_value: Any) -> None:
		return self._execute_function("Debugger.setReturnValue", locals())
	
	def set_script_source(
			self,
			script_id: str,
			script_source: str,
			dry_run: Optional[bool] = None,
			allow_top_frame_editing: Optional[bool] = None
	) -> Tuple[Optional[List[Any]]]:
		return self._execute_function("Debugger.setScriptSource", locals())
	
	def set_skip_all_pauses(self, skip: bool) -> None:
		return self._execute_function("Debugger.setSkipAllPauses", locals())
	
	def set_variable_value(
			self,
			scope_number: int,
			variable_name: str,
			new_value: Any,
			call_frame_id: str
	) -> None:
		return self._execute_function("Debugger.setVariableValue", locals())
	
	def step_into(
			self,
			break_on_async_call: Optional[bool] = None,
			skip_list: Optional[List[Any]] = None
	) -> None:
		return self._execute_function("Debugger.stepInto", locals())
	
	def step_out(self) -> None:
		return self._execute_function("Debugger.stepOut", locals())
	
	def step_over(self, skip_list: Optional[List[Any]] = None) -> None:
		return self._execute_function("Debugger.stepOver", locals())
