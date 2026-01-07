from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.debugger import (
	AbstractDebuggerCDPExecutor
)


class DebuggerCDPExecutor(AbstractDebuggerCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def continue_to_location(self, location: Any, target_call_frames: Optional[str] = None) -> None:
		return await self._execute_function("Debugger.continueToLocation", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("Debugger.disable", locals())
	
	async def disassemble_wasm_module(self, script_id: str) -> Tuple[Optional[str]]:
		return await self._execute_function("Debugger.disassembleWasmModule", locals())
	
	async def enable(self, max_scripts_cache_size: Optional[float] = None) -> str:
		return await self._execute_function("Debugger.enable", locals())
	
	async def evaluate_on_call_frame(
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
		return await self._execute_function("Debugger.evaluateOnCallFrame", locals())
	
	async def get_possible_breakpoints(
			self,
			start: Any,
			end: Optional[Any] = None,
			restrict_to_function: Optional[bool] = None
	) -> List[Any]:
		return await self._execute_function("Debugger.getPossibleBreakpoints", locals())
	
	async def get_script_source(self, script_id: str) -> Tuple[str]:
		return await self._execute_function("Debugger.getScriptSource", locals())
	
	async def get_stack_trace(self, stack_trace_id: Any) -> List[Any]:
		return await self._execute_function("Debugger.getStackTrace", locals())
	
	async def get_wasm_bytecode(self, script_id: str) -> str:
		return await self._execute_function("Debugger.getWasmBytecode", locals())
	
	async def next_wasm_disassembly_chunk(self, stream_id: str) -> List[Any]:
		return await self._execute_function("Debugger.nextWasmDisassemblyChunk", locals())
	
	async def pause(self) -> None:
		return await self._execute_function("Debugger.pause", locals())
	
	async def pause_on_async_call(self, parent_stack_trace_id: Any) -> None:
		return await self._execute_function("Debugger.pauseOnAsyncCall", locals())
	
	async def remove_breakpoint(self, breakpoint_id: str) -> None:
		return await self._execute_function("Debugger.removeBreakpoint", locals())
	
	async def restart_frame(self, call_frame_id: str, mode: Optional[str] = None) -> Tuple[List[Any]]:
		return await self._execute_function("Debugger.restartFrame", locals())
	
	async def resume(self, terminate_on_resume: Optional[bool] = None) -> None:
		return await self._execute_function("Debugger.resume", locals())
	
	async def search_in_content(
			self,
			script_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Any]:
		return await self._execute_function("Debugger.searchInContent", locals())
	
	async def set_async_call_stack_depth(self, max_depth: int) -> None:
		return await self._execute_function("Debugger.setAsyncCallStackDepth", locals())
	
	async def set_blackbox_execution_contexts(self, unique_ids: List[str]) -> None:
		return await self._execute_function("Debugger.setBlackboxExecutionContexts", locals())
	
	async def set_blackbox_patterns(self, patterns: List[str], skip_anonymous: Optional[bool] = None) -> None:
		return await self._execute_function("Debugger.setBlackboxPatterns", locals())
	
	async def set_blackboxed_ranges(self, script_id: str, positions: List[Any]) -> None:
		return await self._execute_function("Debugger.setBlackboxedRanges", locals())
	
	async def set_breakpoint(self, location: Any, condition: Optional[str] = None) -> Tuple[str]:
		return await self._execute_function("Debugger.setBreakpoint", locals())
	
	async def set_breakpoint_by_url(
			self,
			line_number: int,
			url: Optional[str] = None,
			url_regex: Optional[str] = None,
			script_hash: Optional[str] = None,
			column_number: Optional[int] = None,
			condition: Optional[str] = None
	) -> Tuple[str]:
		return await self._execute_function("Debugger.setBreakpointByUrl", locals())
	
	async def set_breakpoint_on_function_call(self, object_id: str, condition: Optional[str] = None) -> str:
		return await self._execute_function("Debugger.setBreakpointOnFunctionCall", locals())
	
	async def set_breakpoints_active(self, active: bool) -> None:
		return await self._execute_function("Debugger.setBreakpointsActive", locals())
	
	async def set_instrumentation_breakpoint(self, instrumentation: str) -> str:
		return await self._execute_function("Debugger.setInstrumentationBreakpoint", locals())
	
	async def set_pause_on_exceptions(self, state: str) -> None:
		return await self._execute_function("Debugger.setPauseOnExceptions", locals())
	
	async def set_return_value(self, new_value: Any) -> None:
		return await self._execute_function("Debugger.setReturnValue", locals())
	
	async def set_script_source(
			self,
			script_id: str,
			script_source: str,
			dry_run: Optional[bool] = None,
			allow_top_frame_editing: Optional[bool] = None
	) -> Tuple[Optional[List[Any]]]:
		return await self._execute_function("Debugger.setScriptSource", locals())
	
	async def set_skip_all_pauses(self, skip: bool) -> None:
		return await self._execute_function("Debugger.setSkipAllPauses", locals())
	
	async def set_variable_value(
			self,
			scope_number: int,
			variable_name: str,
			new_value: Any,
			call_frame_id: str
	) -> None:
		return await self._execute_function("Debugger.setVariableValue", locals())
	
	async def step_into(
			self,
			break_on_async_call: Optional[bool] = None,
			skip_list: Optional[List[Any]] = None
	) -> None:
		return await self._execute_function("Debugger.stepInto", locals())
	
	async def step_out(self) -> None:
		return await self._execute_function("Debugger.stepOut", locals())
	
	async def step_over(self, skip_list: Optional[List[Any]] = None) -> None:
		return await self._execute_function("Debugger.stepOver", locals())
