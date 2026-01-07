from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.runtime import (
	AbstractRuntimeCDPExecutor
)


class RuntimeCDPExecutor(AbstractRuntimeCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_binding(
			self,
			name: str,
			execution_context_id: Optional[int] = None,
			execution_context_name: Optional[str] = None
	) -> None:
		return await self._execute_function("Runtime.addBinding", locals())
	
	async def await_promise(
			self,
			promise_object_id: str,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None
	) -> Tuple[Any, Optional[Any]]:
		return await self._execute_function("Runtime.awaitPromise", locals())
	
	async def call_function_on(
			self,
			function_declaration: str,
			object_id: Optional[str] = None,
			arguments: Optional[List[Any]] = None,
			silent: Optional[bool] = None,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			user_gesture: Optional[bool] = None,
			await_promise: Optional[bool] = None,
			execution_context_id: Optional[int] = None,
			object_group: Optional[str] = None,
			throw_on_side_effect: Optional[bool] = None,
			unique_context_id: Optional[str] = None,
			serialization_options: Optional[Any] = None
	) -> Tuple[Any, Optional[Any]]:
		return await self._execute_function("Runtime.callFunctionOn", locals())
	
	async def compile_script(
			self,
			expression: str,
			source_url: str,
			persist_script: bool,
			execution_context_id: Optional[int] = None
	) -> Tuple[Optional[str], Optional[Any]]:
		return await self._execute_function("Runtime.compileScript", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("Runtime.disable", locals())
	
	async def discard_console_entries(self) -> None:
		return await self._execute_function("Runtime.discardConsoleEntries", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Runtime.enable", locals())
	
	async def evaluate(
			self,
			expression: str,
			object_group: Optional[str] = None,
			include_command_line_api: Optional[bool] = None,
			silent: Optional[bool] = None,
			context_id: Optional[int] = None,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			user_gesture: Optional[bool] = None,
			await_promise: Optional[bool] = None,
			throw_on_side_effect: Optional[bool] = None,
			timeout: Optional[float] = None,
			disable_breaks: Optional[bool] = None,
			repl_mode: Optional[bool] = None,
			allow_unsafe_eval_blocked_by_csp: Optional[bool] = None,
			unique_context_id: Optional[str] = None,
			serialization_options: Optional[Any] = None
	) -> Tuple[Any, Optional[Any]]:
		return await self._execute_function("Runtime.evaluate", locals())
	
	async def get_exception_details(self, error_object_id: str) -> Optional[Any]:
		return await self._execute_function("Runtime.getExceptionDetails", locals())
	
	async def get_heap_usage(self) -> Tuple[float, float, float, float]:
		return await self._execute_function("Runtime.getHeapUsage", locals())
	
	async def get_isolate_id(self) -> str:
		return await self._execute_function("Runtime.getIsolateId", locals())
	
	async def get_properties(
			self,
			object_id: str,
			own_properties: Optional[bool] = None,
			accessor_properties_only: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			non_indexed_properties_only: Optional[bool] = None
	) -> Tuple[List[Any], Optional[List[Any]], Optional[List[Any]], Optional[Any]]:
		return await self._execute_function("Runtime.getProperties", locals())
	
	async def global_lexical_scope_names(self, execution_context_id: Optional[int] = None) -> List[str]:
		return await self._execute_function("Runtime.globalLexicalScopeNames", locals())
	
	async def query_objects(self, prototype_object_id: str, object_group: Optional[str] = None) -> Any:
		return await self._execute_function("Runtime.queryObjects", locals())
	
	async def release_object(self, object_id: str) -> None:
		return await self._execute_function("Runtime.releaseObject", locals())
	
	async def release_object_group(self, object_group: str) -> None:
		return await self._execute_function("Runtime.releaseObjectGroup", locals())
	
	async def remove_binding(self, name: str) -> None:
		return await self._execute_function("Runtime.removeBinding", locals())
	
	async def run_if_waiting_for_debugger(self) -> None:
		return await self._execute_function("Runtime.runIfWaitingForDebugger", locals())
	
	async def run_script(
			self,
			script_id: str,
			execution_context_id: Optional[int] = None,
			object_group: Optional[str] = None,
			silent: Optional[bool] = None,
			include_command_line_api: Optional[bool] = None,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			await_promise: Optional[bool] = None
	) -> Tuple[Any, Optional[Any]]:
		return await self._execute_function("Runtime.runScript", locals())
	
	async def set_async_call_stack_depth(self, max_depth: int) -> None:
		return await self._execute_function("Runtime.setAsyncCallStackDepth", locals())
	
	async def set_custom_object_formatter_enabled(self, enabled: bool) -> None:
		return await self._execute_function("Runtime.setCustomObjectFormatterEnabled", locals())
	
	async def set_max_call_stack_size_to_capture(self, size: int) -> None:
		return await self._execute_function("Runtime.setMaxCallStackSizeToCapture", locals())
	
	async def terminate_execution(self) -> None:
		return await self._execute_function("Runtime.terminateExecution", locals())
