import trio
from typing import Any, Dict, Optional
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.client_config import ClientConfig
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.trio_bidi._typehints import (
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi._models import (
	W3CTask,
	W3CTaskContainer
)
from osn_selenium.trio_bidi._context_vars import (
	CURRENT_BROWSING_CONTEXT
)
from osn_selenium.trio_bidi._internal_mappings import (
	OSN_SWITCH_CONTEXT_KEY
)


__all__ = ["BiDiBridgeRemoteConnection"]


def _processing_in_trio_loop() -> bool:
	"""
	Checks if the current code is executing within a Trio event loop.

	Returns:
		bool: True if in a Trio loop, False otherwise.
	"""
	
	is_in_trio = False
	
	try:
		trio.lowlevel.current_task()
		is_in_trio = True
	except RuntimeError:
		pass
	
	return is_in_trio


def _handle_response(w3c_task_container: W3CTaskContainer) -> Dict[str, Any]:
	"""
	Processes the result of a W3C task, handling errors and context switching.

	Args:
		w3c_task_container (W3CTaskContainer): The container holding the task result.

	Returns:
		Dict[str, Any]: The processed W3C response.

	Raises:
		Exception: The error received from the BiDi bridge if the task failed.
	"""
	
	if w3c_task_container.response["error"]:
		raise w3c_task_container.response["error"]
	
	osn_switch_context_value = w3c_task_container.response["response"].get(OSN_SWITCH_CONTEXT_KEY, None)
	if osn_switch_context_value is not None:
		CURRENT_BROWSING_CONTEXT.set(osn_switch_context_value)
	
	return w3c_task_container.response["response"]


class BiDiBridgeRemoteConnection(RemoteConnection):
	"""
	Remote connection implementation that bridges W3C commands to a BiDi-capable backend via Trio.
	"""
	
	def __init__(
			self,
			send_channel: trio.MemorySendChannel[W3CTaskContainer],
			trio_token: trio.lowlevel.TrioToken,
			legacy_remote_connection: RemoteConnection,
			remote_server_addr: Optional[str] = "http://localhost:9999",
			keep_alive: bool = True,
			ignore_proxy: bool = False,
			ignore_certificates: Optional[bool] = False,
			init_args_for_pool_manager: Optional[Dict] = None,
			client_config: Optional[ClientConfig] = None,
	):
		"""
		Initializes the BiDiBridgeRemoteConnection.

		Args:
			send_channel (trio.MemorySendChannel[W3CTaskContainer]): The channel to send W3C tasks to.
			trio_token (trio.lowlevel.TrioToken): The token for the Trio event loop.
			legacy_remote_connection (RemoteConnection): The underlying legacy connection.
			remote_server_addr (Optional[str]): The address of the remote Selenium server.
			keep_alive (bool): Whether to keep the connection alive.
			ignore_proxy (bool): Whether to ignore proxy settings.
			ignore_certificates (Optional[bool]): Whether to ignore SSL certificate errors.
			init_args_for_pool_manager (Optional[Dict]): Additional arguments for the pool manager.
			client_config (Optional[ClientConfig]): Configuration object for the client.
		"""
		
		super().__init__(
				remote_server_addr=remote_server_addr,
				keep_alive=keep_alive,
				ignore_proxy=ignore_proxy,
				ignore_certificates=ignore_certificates,
				init_args_for_pool_manager=init_args_for_pool_manager,
				client_config=client_config,
		)
		
		self._legacy_remote_connection = legacy_remote_connection
		self._trio_send_channel = send_channel
		self._trio_token = trio_token
	
	def _OSN_GET_CURRENT_WINDOW_HANDLE(self, command: str, params: REQUEST_PARAMS_TYPEHINT) -> Optional[str]:
		"""
		Internal method to manage browsing context handle via local cache or legacy call.

		Args:
			command (str): Current command name.
			params (Optional[Dict[str, Any]]): Current command parameters.

		Returns:
			Optional[str]: The browsing context ID.
		"""
		
		context_id = CURRENT_BROWSING_CONTEXT.get()
		
		if context_id is not None:
			return context_id
		
		context_id = self._legacy_remote_connection.execute(command, params)["value"]
		CURRENT_BROWSING_CONTEXT.set(context_id)
		
		return context_id
	
	def execute(self, command: str, params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
		"""
		Executes a W3C command by sending it through the BiDi bridge or legacy connection.

		Args:
			command (str): The name of the command to execute.
			params (Optional[Dict[str, Any]]): The parameters for the command.

		Returns:
			Dict[str, Any]: The response from the remote end.
		"""
		
		if _processing_in_trio_loop():
			return self._legacy_remote_connection.execute(command, params)
		
		context_id = self._OSN_GET_CURRENT_WINDOW_HANDLE(command=command, params=params)
		
		if command == Command.W3C_GET_CURRENT_WINDOW_HANDLE:
			return {"value": context_id}
		
		w3c_task_container = W3CTaskContainer(task=W3CTask(command=command, params=params, context_id=context_id))
		
		trio.from_thread.run(
				self._trio_send_channel.send,
				w3c_task_container,
				trio_token=self._trio_token
		)
		
		w3c_task_container.pending_event.wait()
		
		return _handle_response(w3c_task_container=w3c_task_container)
