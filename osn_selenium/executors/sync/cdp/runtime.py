from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.runtime import (
	UnifiedRuntimeCDPExecutor
)
from osn_selenium.abstract.executors.cdp.runtime import (
	AbstractRuntimeCDPExecutor
)


__all__ = ["RuntimeCDPExecutor"]


class RuntimeCDPExecutor(UnifiedRuntimeCDPExecutor, AbstractRuntimeCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedRuntimeCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_binding(
			self,
			name: str,
			execution_context_id: Optional[int] = None,
			execution_context_name: Optional[str] = None
	) -> None:
		return self._add_binding_impl(
				name=name,
				execution_context_id=execution_context_id,
				execution_context_name=execution_context_name
		)
	
	def await_promise(
			self,
			promise_object_id: str,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None
	) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
		return self._await_promise_impl(
				promise_object_id=promise_object_id,
				return_by_value=return_by_value,
				generate_preview=generate_preview
		)
	
	def call_function_on(
			self,
			function_declaration: str,
			object_id: Optional[str] = None,
			arguments: Optional[List[Dict[str, Any]]] = None,
			silent: Optional[bool] = None,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			user_gesture: Optional[bool] = None,
			await_promise: Optional[bool] = None,
			execution_context_id: Optional[int] = None,
			object_group: Optional[str] = None,
			throw_on_side_effect: Optional[bool] = None,
			unique_context_id: Optional[str] = None,
			serialization_options: Optional[Dict[str, Any]] = None
	) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
		return self._call_function_on_impl(
				function_declaration=function_declaration,
				object_id=object_id,
				arguments=arguments,
				silent=silent,
				return_by_value=return_by_value,
				generate_preview=generate_preview,
				user_gesture=user_gesture,
				await_promise=await_promise,
				execution_context_id=execution_context_id,
				object_group=object_group,
				throw_on_side_effect=throw_on_side_effect,
				unique_context_id=unique_context_id,
				serialization_options=serialization_options
		)
	
	def compile_script(
			self,
			expression: str,
			source_url: str,
			persist_script: bool,
			execution_context_id: Optional[int] = None
	) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
		return self._compile_script_impl(
				expression=expression,
				source_url=source_url,
				persist_script=persist_script,
				execution_context_id=execution_context_id
		)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def discard_console_entries(self) -> None:
		return self._discard_console_entries_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def evaluate(
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
			serialization_options: Optional[Dict[str, Any]] = None
	) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
		return self._evaluate_impl(
				expression=expression,
				object_group=object_group,
				include_command_line_api=include_command_line_api,
				silent=silent,
				context_id=context_id,
				return_by_value=return_by_value,
				generate_preview=generate_preview,
				user_gesture=user_gesture,
				await_promise=await_promise,
				throw_on_side_effect=throw_on_side_effect,
				timeout=timeout,
				disable_breaks=disable_breaks,
				repl_mode=repl_mode,
				allow_unsafe_eval_blocked_by_csp=allow_unsafe_eval_blocked_by_csp,
				unique_context_id=unique_context_id,
				serialization_options=serialization_options
		)
	
	def get_exception_details(self, error_object_id: str) -> Optional[Dict[str, Any]]:
		return self._get_exception_details_impl(error_object_id=error_object_id)
	
	def get_heap_usage(self) -> Tuple[float, float, float, float]:
		return self._get_heap_usage_impl()
	
	def get_isolate_id(self) -> str:
		return self._get_isolate_id_impl()
	
	def get_properties(
			self,
			object_id: str,
			own_properties: Optional[bool] = None,
			accessor_properties_only: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			non_indexed_properties_only: Optional[bool] = None
	) -> Tuple[
		List[Dict[str, Any]],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[Dict[str, Any]]
	]:
		return self._get_properties_impl(
				object_id=object_id,
				own_properties=own_properties,
				accessor_properties_only=accessor_properties_only,
				generate_preview=generate_preview,
				non_indexed_properties_only=non_indexed_properties_only
		)
	
	def global_lexical_scope_names(self, execution_context_id: Optional[int] = None) -> List[str]:
		return self._global_lexical_scope_names_impl(execution_context_id=execution_context_id)
	
	def query_objects(self, prototype_object_id: str, object_group: Optional[str] = None) -> Dict[str, Any]:
		return self._query_objects_impl(prototype_object_id=prototype_object_id, object_group=object_group)
	
	def release_object(self, object_id: str) -> None:
		return self._release_object_impl(object_id=object_id)
	
	def release_object_group(self, object_group: str) -> None:
		return self._release_object_group_impl(object_group=object_group)
	
	def remove_binding(self, name: str) -> None:
		return self._remove_binding_impl(name=name)
	
	def run_if_waiting_for_debugger(self) -> None:
		return self._run_if_waiting_for_debugger_impl()
	
	def run_script(
			self,
			script_id: str,
			execution_context_id: Optional[int] = None,
			object_group: Optional[str] = None,
			silent: Optional[bool] = None,
			include_command_line_api: Optional[bool] = None,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None,
			await_promise: Optional[bool] = None
	) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
		return self._run_script_impl(
				script_id=script_id,
				execution_context_id=execution_context_id,
				object_group=object_group,
				silent=silent,
				include_command_line_api=include_command_line_api,
				return_by_value=return_by_value,
				generate_preview=generate_preview,
				await_promise=await_promise
		)
	
	def set_async_call_stack_depth(self, max_depth: int) -> None:
		return self._set_async_call_stack_depth_impl(max_depth=max_depth)
	
	def set_custom_object_formatter_enabled(self, enabled: bool) -> None:
		return self._set_custom_object_formatter_enabled_impl(enabled=enabled)
	
	def set_max_call_stack_size_to_capture(self, size: int) -> None:
		return self._set_max_call_stack_size_to_capture_impl(size=size)
	
	def terminate_execution(self) -> None:
		return self._terminate_execution_impl()
