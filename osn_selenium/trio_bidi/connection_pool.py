import sys
import json
import math
import trio
import traceback
import itertools
from types import TracebackType
from contextlib import AsyncExitStack
from osn_selenium._decorators import log_on_error
from osn_selenium.trio_bidi._file_functions import unzip_file
from typing import (
	Any,
	Dict,
	Optional,
	Tuple,
	Type,
	Union
)
from trio_websocket import (
	WebSocketConnection,
	open_websocket_url
)
from osn_selenium.trio_bidi.mapping.request_functions import map_request
from osn_selenium.trio_bidi.mapping.response_functions import map_response
from osn_selenium.exceptions.bidi_bridge import (
	BiDiBridgeStoppedError
)
from osn_selenium.trio_bidi._error_redirects import (
	redirect_error_response
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT
)
from osn_selenium.exceptions.devtools import (
	TrioEndExceptions,
	WebSocketEndExceptions
)
from osn_selenium.trio_bidi._models import (
	BiDiTask,
	BiDiTaskContainer,
	W3CTask,
	W3CTaskContainer
)
from osn_selenium.trio_bidi._internal_mappings import (
	GET_INTERNAL_ALERT_TEXT,
	UPLOAD_INTERNAL_FILE
)


__all__ = ["BiDiConnectionPool"]


class _WebsocketResponseHandler:
	"""
	Internal handler for reading and dispatching WebSocket messages.
	"""
	
	def __init__(self, connection_pool: "BiDiConnectionPool"):
		"""
		Initializes the response handler.

		Args:
			connection_pool (BiDiConnectionPool): The parent connection pool.
		"""
		
		self._connection_pool = connection_pool
	
	async def _handle_normal_response(self, response_data: Dict[str, Any]) -> bool:
		"""
		Handles responses for specific BiDi tasks.

		Args:
			response_data (Dict[str, Any]): The response data from BiDi.

		Returns:
			bool: True if the response was handled, False otherwise.
		"""
		
		id_ = response_data.get("id", None)
		
		if id_ in self._connection_pool.bidi_tasks_containers:
			self._connection_pool.bidi_tasks_containers[id_].response = response_data
			self._connection_pool.bidi_tasks_containers[id_].pending_event.set()
		
			return True
		
		return False
	
	async def _handle_user_prompt_response(self, response_data: Dict[str, Any]) -> bool:
		"""
		Handles user prompt events from BiDi.

		Args:
			response_data (Dict[str, Any]): The response data from BiDi.

		Returns:
			bool: True if the response was a user prompt event, False otherwise.
		"""
		
		method = response_data.get("method")
		params = response_data.get("params", {})
		
		if method == "browsingContext.userPromptOpened":
			context = params.get("context")
			message = params.get("message", "")
		
			self._connection_pool.active_prompts[context] = message
		
			return True
		
		if method == "browsingContext.userPromptClosed":
			context = params.get("context")
		
			self._connection_pool.active_prompts.pop(context, None)
		
			return True
		
		return False
	
	async def _handle_response(self, response_data: Dict[str, Any]) -> None:
		"""
		Dispatches BiDi responses to appropriate handlers.

		Args:
			response_data (Dict[str, Any]): The response data from BiDi.
		"""
		
		if await self._handle_user_prompt_response(response_data=response_data):
			return
		
		if await self._handle_normal_response(response_data=response_data):
			return
	
	async def run(self):
		"""
		Continuously reads messages from the WebSocket and handles them.
		"""
		
		while True:
			try:
				message = await self._connection_pool.websocket_connection.get_message()
				response_data: Dict[str, Any] = json.loads(message)
		
				await self._handle_response(response_data=response_data)
			except WebSocketEndExceptions:
				break


class _TaskHandler:
	"""
	Internal handler for processing W3C tasks and executing BiDi commands.
	"""
	
	def __init__(self, connection_pool: "BiDiConnectionPool"):
		"""
		Initializes the task handler.

		Args:
			connection_pool (BiDiConnectionPool): The parent connection pool.
		"""
		
		self._connection_pool = connection_pool
	
	def _create_bidi_task_container(self, bidi_request: Dict[str, Any]) -> Tuple[int, BiDiTaskContainer]:
		"""
		Creates a container for a BiDi task.

		Args:
			bidi_request (Dict[str, Any]): The BiDi request parameters.

		Returns:
			Tuple[int, BiDiTaskContainer]: The bridge container ID and the task container.
		"""
		
		bridge_container_id = next(self._connection_pool.id_generator)
		bidi_task = BiDiTask(
				id=bridge_container_id,
				method=bidi_request["method"],
				params=bidi_request["params"]
		)
		
		return bridge_container_id, BiDiTaskContainer(task=bidi_task)
	
	async def _send_request_to_bidi(self, bidi_request: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Sends a request to BiDi and waits for the response.

		Args:
			bidi_request (Dict[str, Any]): The request to send.

		Returns:
			Dict[str, Any]: The BiDi response.
		"""
		
		bridge_container_id, bidi_task_container = self._create_bidi_task_container(bidi_request=bidi_request)
		self._connection_pool.bidi_tasks_containers[bridge_container_id] = bidi_task_container
		
		await self._connection_pool.websocket_connection.send_message(json.dumps(bidi_task_container.task.to_dict()))
		await self._connection_pool.bidi_tasks_containers[bridge_container_id].pending_event.wait()
		
		bidi_task_container = self._connection_pool.bidi_tasks_containers.pop(bridge_container_id)
		bidi_response = bidi_task_container.response
		
		return bidi_response
	
	async def _get_normal_response(self, bidi_request: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Handles a general BiDi task.

		Args:
			bidi_request (Dict[str, Any]): The request parameters.

		Returns:
			Dict[str, Any]: The BiDi response.
		"""
		
		bidi_response = await self._send_request_to_bidi(bidi_request=bidi_request)
		
		return bidi_response
	
	@staticmethod
	async def _get_uploaded_file(bidi_request: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Handles the task of uploading a file.

		Args:
			bidi_request (Dict[str, Any]): The BiDi request containing the file data.

		Returns:
			Dict[str, Any]: The response containing the extracted file path.
		"""
		
		return {"result": {"value": unzip_file(base64_zip=bidi_request["file"])}}
	
	async def _get_context_user_prompt_text(self, context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT) -> Dict[str, Any]:
		"""
		Handles the task of retrieving text from a user prompt.

		Args:
			context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The ID of the browsing context.

		Returns:
			Dict[str, Any]: The response containing the prompt text.
		"""
		
		text = self._connection_pool.active_prompts.get(context_id, None)
		
		if text is None:
			return {"error": "no such alert", "message": "no such alert"}
		
		return {"result": {"value": text}}
	
	async def _get_task_response(self, bidi_request: Dict[str, Any], w3c_task: W3CTask) -> Dict[str, Any]:
		"""
		Dispatches request to appropriate execution method.

		Args:
			bidi_request (Dict[str, Any]): The request to execute.
			w3c_task (W3CTask): The original W3C task.

		Returns:
			Dict[str, Any]: The raw BiDi response.
		"""
		
		bidi_method = bidi_request.get("method")
		
		if bidi_method == GET_INTERNAL_ALERT_TEXT:
			return await self._get_context_user_prompt_text(context_id=w3c_task.context_id)
		
		if bidi_method == UPLOAD_INTERNAL_FILE:
			return await self._get_uploaded_file(bidi_request=bidi_request)
		
		return await self._get_normal_response(bidi_request=bidi_request)
	
	async def _handle_request(self, bidi_request: Dict[str, Any], w3c_task: W3CTask) -> Dict[str, Any]:
		"""
		Executes BiDi request and maps it back to W3C response.

		Args:
			bidi_request (Dict[str, Any]): The mapped BiDi request.
			w3c_task (W3CTask): The original W3C task.

		Returns:
			Dict[str, Any]: The W3C-compatible response.
		"""
		
		bidi_response = await self._get_task_response(bidi_request=bidi_request, w3c_task=w3c_task)
		
		if "error" in bidi_response:
			return redirect_error_response(command=w3c_task.command, bidi_response=bidi_response)
		
		return map_response(
				command=w3c_task.command,
				bidi_result=bidi_response["result"],
				request_params=w3c_task.params
		)
	
	async def _handle_task(self, w3c_task_container: W3CTaskContainer):
		"""
		Processes a W3C task by mapping it to BiDi and executing it.

		Args:
			w3c_task_container (W3CTaskContainer): The container of the W3C task to process.
		"""
		
		try:
			w3c_task = w3c_task_container.task
		
			bidi_request = map_request(
					command=w3c_task.command,
					params=w3c_task.params,
					context_id=w3c_task.context_id
			)
		
			w3c_task_container.response["response"] = await self._handle_request(bidi_request=bidi_request, w3c_task=w3c_task)
		except Exception as exception:
			w3c_task_container.response["error"] = exception
		finally:
			w3c_task_container.pending_event.set()
	
	async def run(self) -> None:
		"""
		Processes W3C tasks from the receive channel.
		"""
		
		try:
			async for w3c_task_container in self._connection_pool.task_receive_channel:
				self._connection_pool.nursery.start_soon(self._handle_task, w3c_task_container)
		except WebSocketEndExceptions:
			pass


class BiDiConnectionPool:
	"""
	Manages a pool of connections and tasks for BiDi communication.
	"""
	
	def __init__(self, websocket_url: str, buffer_size: Union[int, float] = math.inf):
		"""
		Initializes the BiDiConnectionPool.

		Args:
			websocket_url (str): The URL of the WebSocket server.
			buffer_size (Union[int, float]): The size of the task buffer.
		"""
		
		self._websocket_url = websocket_url
		self._buffer_size = buffer_size
		self._websocket_connection: Optional[WebSocketConnection] = None
		self._nursery: Optional[trio.Nursery] = None
		self._exit_stack = AsyncExitStack()
		self._task_send_channel: Optional[trio.MemorySendChannel[W3CTaskContainer]] = None
		self._task_receive_channel: Optional[trio.MemoryReceiveChannel[W3CTaskContainer]] = None
		self._id_generator: Optional[itertools.count[int]] = None
		self._bidi_tasks_containers: Dict[int, BiDiTaskContainer] = {}
		self._active_prompts: Dict[str, str] = {}
		self._is_active = False
		
		self._task_handler = _TaskHandler(connection_pool=self)
		
		self._response_handler = _WebsocketResponseHandler(connection_pool=self)
	
	async def start(self) -> trio.MemorySendChannel[W3CTaskContainer]:
		"""
		Starts the connection pool and internal loops.

		Returns:
			trio.MemorySendChannel[W3CTaskContainer]: The channel to send tasks to.
		"""
		
		if self._is_active:
			return self._task_send_channel
		
		self._websocket_connection = await self._exit_stack.enter_async_context(open_websocket_url(self._websocket_url))
		self._nursery = await self._exit_stack.enter_async_context(trio.open_nursery())
		
		self._task_send_channel, self._task_receive_channel = trio.open_memory_channel(max_buffer_size=self._buffer_size)
		
		self._nursery.start_soon(self._task_handler.run)
		self._nursery.start_soon(self._response_handler.run)
		
		self._id_generator = itertools.count(1)
		self._is_active = True
		
		return self._task_send_channel
	
	async def __aenter__(self) -> trio.MemorySendChannel[W3CTaskContainer]:
		"""
		Async context manager entry.

		Returns:
			trio.MemorySendChannel[W3CTaskContainer]: The task send channel.
		"""
		
		return await self.start()
	
	async def stop(self) -> None:
		"""
		Stops the connection pool and cleans up resources.
		"""
		
		@log_on_error
		async def _close_channels() -> None:
			"""
			Closes the task send and receive memory channels.
			"""
			
			if self._task_send_channel is not None:
				try:
					await self._task_send_channel.aclose()
				except TrioEndExceptions:
					pass
			
				self._task_send_channel = None
			
			if self._task_receive_channel is not None:
				try:
					await self._task_receive_channel.aclose()
				except TrioEndExceptions:
					pass
			
				self._task_receive_channel = None
		
		@log_on_error
		async def _close_bidi_tasks() -> None:
			"""
			Cleans up pending BiDi tasks by setting a stop error and clearing the containers.
			"""
			
			if exc_type is not None or exc_value is not None or exc_traceback is not None:
				reason = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
			else:
				reason = "BiDi connection pool stopped"
			
			for container in self._bidi_tasks_containers.values():
				if not container.pending_event.is_set():
					container.response["error"] = BiDiBridgeStoppedError(reason=reason)
					container.pending_event.set()
			
			self._bidi_tasks_containers.clear()
		
		@log_on_error
		async def _close_async_stack() -> None:
			"""
			Closes the asynchronous resource stack.
			"""
			
			if self._nursery is not None:
				try:
					self._nursery.cancel_scope.cancel()
				except TrioEndExceptions:
					pass
			
				self._nursery = None
			
			if self._websocket_connection is not None:
				try:
					await self._websocket_connection.aclose()
				except TrioEndExceptions:
					pass
			
				self._websocket_connection = None
			
			try:
				await self._exit_stack.aclose()
			except TrioEndExceptions:
				pass
			except AssertionError:
				pass  # TODO solve exit issue
		
		exc_type, exc_value, exc_traceback = sys.exc_info()
		
		if not self._is_active:
			return
		
		await _close_channels()
		await _close_bidi_tasks()
		await _close_async_stack()
		
		self._active_prompts.clear()
		self._id_generator = None
		self._is_active = False
	
	async def __aexit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType],
	) -> bool:
		"""
		Asynchronously exits the BiDi connection pool context.

		Args:
			exc_type (Optional[Type[BaseException]]): The exception type, if any.
			exc_val (Optional[BaseException]): The exception value, if any.
			exc_tb (Optional[TracebackType]): The exception traceback, if any.

		Returns:
			bool: True if an exception was suppressed, False otherwise.
		"""
		
		await self.stop()
		
		if exc_type is not None and exc_val is not None and exc_tb is not None:
			return True
		
		return False
	
	@property
	def active_prompts(self) -> Dict[str, str]:
		"""
		Returns the map of active prompts.
		"""
		
		return self._active_prompts
	
	@property
	def bidi_tasks_containers(self) -> Dict[int, BiDiTaskContainer]:
		"""
		Returns the active BiDi tasks.
		"""
		
		return self._bidi_tasks_containers
	
	@property
	def buffer_size(self) -> Union[int, float]:
		"""
		Returns the buffer size.
		"""
		
		return self._buffer_size
	
	@property
	def id_generator(self) -> Optional[itertools.count]:
		"""
		Returns the task ID generator.
		"""
		
		return self._id_generator
	
	@property
	def is_active(self) -> bool:
		"""
		Returns the activation status.
		"""
		
		return self._is_active
	
	@property
	def nursery(self) -> Optional[trio.Nursery]:
		"""
		Returns the internal nursery.
		"""
		
		return self._nursery
	
	@property
	def task_receive_channel(self) -> trio.MemoryReceiveChannel[W3CTaskContainer]:
		"""
		Returns the task receive channel.
		"""
		
		return self._task_receive_channel
	
	@property
	def task_send_channel(self) -> trio.MemorySendChannel[W3CTaskContainer]:
		"""
		Returns the task send channel.
		"""
		
		return self._task_send_channel
	
	@property
	def websocket_connection(self) -> Optional[WebSocketConnection]:
		"""
		Returns the current WebSocket connection.
		"""
		
		return self._websocket_connection
	
	@property
	def websocket_url(self) -> str:
		"""
		Returns the WebSocket URL.
		"""
		
		return self._websocket_url
