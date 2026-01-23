from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractRuntimeCDPExecutor"]


class AbstractRuntimeCDPExecutor(ABC):
	@abstractmethod
	def add_binding(
			self,
			name: str,
			execution_context_id: Optional[int] = None,
			execution_context_name: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def await_promise(
			self,
			promise_object_id: str,
			return_by_value: Optional[bool] = None,
			generate_preview: Optional[bool] = None
	) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def compile_script(
			self,
			expression: str,
			source_url: str,
			persist_script: bool,
			execution_context_id: Optional[int] = None
	) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def discard_console_entries(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def get_exception_details(self, error_object_id: str) -> Optional[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_heap_usage(self) -> Tuple[float, float, float, float]:
		...
	
	@abstractmethod
	def get_isolate_id(self) -> str:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def global_lexical_scope_names(self, execution_context_id: Optional[int] = None) -> List[str]:
		...
	
	@abstractmethod
	def query_objects(self, prototype_object_id: str, object_group: Optional[str] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def release_object(self, object_id: str) -> None:
		...
	
	@abstractmethod
	def release_object_group(self, object_group: str) -> None:
		...
	
	@abstractmethod
	def remove_binding(self, name: str) -> None:
		...
	
	@abstractmethod
	def run_if_waiting_for_debugger(self) -> None:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def set_async_call_stack_depth(self, max_depth: int) -> None:
		...
	
	@abstractmethod
	def set_custom_object_formatter_enabled(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_max_call_stack_size_to_capture(self, size: int) -> None:
		...
	
	@abstractmethod
	def terminate_execution(self) -> None:
		...
