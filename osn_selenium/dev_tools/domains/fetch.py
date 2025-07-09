import trio
from dataclasses import dataclass
from osn_selenium.dev_tools.utils import (
	cdp_end_exceptions,
	execute_cdp_command
)
from osn_selenium.dev_tools.domains_default.fetch import (
	auth_required_choose_func,
	request_paused_choose_func
)
from typing import (
	Any,
	Awaitable,
	Callable,
	Literal,
	Mapping,
	Optional,
	Sequence,
	TYPE_CHECKING,
	TypedDict
)
from osn_selenium.dev_tools.domains.abstract import (
	AbstractAction,
	AbstractActionParametersHandlersSettings,
	AbstractActionSettings,
	AbstractDomain,
	AbstractDomainEnableKwargsSettings,
	AbstractDomainHandlersSettings,
	AbstractDomainSettings,
	AbstractEvent,
	AbstractEventActionsHandler,
	AbstractEventActionsHandlerSettings,
	AbstractEventActionsSettings,
	AbstractEventSettings,
	ParameterHandler,
	build_kwargs_from_handlers_func_type,
	kwargs_type,
	on_error_func_type,
	response_handle_func_type
)


if TYPE_CHECKING:
	from osn_selenium.dev_tools.manager import DevToolsTarget


class _ContinueWithAuthParametersHandlers(TypedDict):
	"""
	Internal TypedDict for handlers related to the 'continueWithAuth' action.

	Attributes:
		response (ParameterHandler): Handler for the auth challenge response.
		username (Optional[ParameterHandler]): Handler for providing the username.
		password (Optional[ParameterHandler]): Handler for providing the password.
	"""
	
	response: ParameterHandler
	username: Optional[ParameterHandler]
	password: Optional[ParameterHandler]


@dataclass
class ContinueWithAuthParameterHandlersSettings(AbstractActionParametersHandlersSettings):
	"""
	Settings for the handlers that provide authentication credentials when required.

	Attributes:
		response (ParameterHandler): Handler for the authentication challenge response. This handler determines the response type (e.g., default, custom credentials, or canceled).
		username (Optional[ParameterHandler]): Optional handler for providing the username if using custom credentials. Defaults to None.
		password (Optional[ParameterHandler]): Optional handler for providing the password if using custom credentials. Defaults to None.
	"""
	
	response: ParameterHandler
	username: Optional[ParameterHandler] = None
	password: Optional[ParameterHandler] = None
	
	def to_dict(self) -> _ContinueWithAuthParametersHandlers:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_ContinueWithAuthParametersHandlers: The dictionary representation suitable for internal use.
		"""
		
		return _ContinueWithAuthParametersHandlers(
				response=self.response,
				username=self.username,
				password=self.password,
		)


async def _build_kwargs_from_handlers_func(
		self: "DevToolsTarget",
		handlers: Mapping[str, Optional[ParameterHandler]],
		event: Any
) -> kwargs_type:
	"""
	Asynchronously builds keyword arguments for a CDP command by executing parameter handlers.

	This function iterates through a mapping of parameter handlers, starting each handler
	in a new Trio task. It waits for all handlers to complete before returning the
	aggregated keyword arguments.

	Args:
		self (DevToolsTarget): the DevToolsTarget instance.
		handlers (Mapping[str, Optional[ParameterHandler]]): A dictionary where keys are parameter names
			and values are `ParameterHandler` objects or None.
		event (Any): The CDP event object that triggered the action, providing context for handlers.

	Returns:
		kwargs_type: A dictionary of keyword arguments ready to be used with a CDP command.

	Raises:
		BaseException: If any error occurs during the execution of parameter handlers or the process.
	"""
	
	await self.log(level="INFO", message=f"Started to build kwargs for '{event}'")
	
	try:
		kwargs = {"request_id": event.request_id}
	
		kwargs_ready_events: list[trio.Event] = []
	
		for handler_name, handler_settings in handlers.items():
			if handler_settings is not None:
				kwargs_ready_event = trio.Event()
				kwargs_ready_events.append(kwargs_ready_event)
	
				self._nursery_object.start_soon(
						handler_settings["func"],
						self,
						kwargs_ready_event,
						handler_settings["instances"],
						event,
						kwargs
				)
	
		for kwargs_ready_event in kwargs_ready_events:
			await kwargs_ready_event.wait()
	
		return kwargs
	except* cdp_end_exceptions as error:
		raise error
	except* BaseException as error:
		await self.log_error(error=error)
		raise error


class _ContinueWithAuth(TypedDict):
	"""
	Internal TypedDict for the 'continueWithAuth' action configuration.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the `continueWithAuth` CDP command.
		response_handle_func (response_handle_func_type): A function to process the response from the CDP command.
		parameters_handlers (_ContinueWithAuthParametersHandlers): Handlers for authentication parameters.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type
	response_handle_func: response_handle_func_type
	parameters_handlers: _ContinueWithAuthParametersHandlers


@dataclass
class ContinueWithAuthSettings(AbstractActionSettings):
	"""
	Settings for continuing a request that requires authentication using the `fetch.continueWithAuth` CDP command.

	Attributes:
		parameters_handlers (ContinueWithAuthParameterHandlersSettings): Settings for the handlers that provide authentication credentials.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.continueWithAuth` CDP command. Defaults to None.
	"""
	
	parameters_handlers: ContinueWithAuthParameterHandlersSettings
	response_handle_func: response_handle_func_type = None
	
	@property
	def kwargs_func(self) -> build_kwargs_from_handlers_func_type:
		"""
		Returns the function used to build keyword arguments for the `continueWithAuth` command.

		Returns:
			build_kwargs_from_handlers_func_type: The internal function `_build_kwargs_from_handlers_func`.
		"""
		
		return _build_kwargs_from_handlers_func
	
	def to_dict(self) -> _ContinueWithAuth:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_ContinueWithAuth: The dictionary representation suitable for internal use.
		"""
		
		return _ContinueWithAuth(
				kwargs_func=self.kwargs_func,
				response_handle_func=self.response_handle_func,
				parameters_handlers=self.parameters_handlers.to_dict(),
		)


class _AuthRequiredActions(TypedDict):
	"""
	Internal TypedDict mapping action names for AuthRequired event to their configurations.

	Attributes:
		continue_with_auth (Optional[_ContinueWithAuth]): Configuration for the 'continueWithAuth' action.
	"""
	
	continue_with_auth: Optional[_ContinueWithAuth]


@dataclass
class AuthRequiredActionsSettings(AbstractEventActionsSettings):
	"""
	Container for configurations of possible actions to take when authentication is required.

	Attributes:
		continue_with_auth (Optional[ContinueWithAuthSettings]): Settings for handling the authentication challenge using `fetch.continueWithAuth`. Defaults to None.
	"""
	
	continue_with_auth: Optional[ContinueWithAuthSettings] = None
	
	def to_dict(self) -> _AuthRequiredActions:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_AuthRequiredActions: The dictionary representation suitable for internal use.
		"""
		
		return _AuthRequiredActions(
				continue_with_auth=self.continue_with_auth.to_dict()
				if self.continue_with_auth is not None
				else None,
		)


class _AuthRequiredActionsHandler(AbstractEventActionsHandler):
	"""
	Internal TypedDict for the actions handler configuration for the 'AuthRequired' event.

	Attributes:
		choose_action_func (auth_required_choose_action_func_type): A function that determines which actions (by name) should be executed for a given 'AuthRequired' event.
		actions (_AuthRequiredActions): A dictionary mapping action names to their full configurations.
	"""
	
	choose_action_func: "auth_required_choose_action_func_type"
	actions: _AuthRequiredActions


@dataclass
class AuthRequiredActionsHandlerSettings(AbstractEventActionsHandlerSettings):
	"""
	Settings for handling the 'fetch.AuthRequired' event by choosing and executing specific actions.

	Attributes:
		choose_action_func (auth_required_choose_action_func_type): A function that takes the DevTools instance and the event object and returns a list of action names (Literals) to execute. Defaults to `auth_required_choose_func`.
		actions (Optional[AuthRequiredActionsSettings]): Container for the configuration of the available actions. Defaults to None.
	"""
	
	choose_action_func: "auth_required_choose_action_func_type" = auth_required_choose_func
	actions: Optional[AuthRequiredActionsSettings] = None
	
	@property
	def kwargs_func(self) -> build_kwargs_from_handlers_func_type:
		"""
		Returns the function used to build keyword arguments for the actions.

		Returns:
			build_kwargs_from_handlers_func_type: The internal function `_build_kwargs_from_handlers_func`.
		"""
		
		return _build_kwargs_from_handlers_func
	
	def to_dict(self) -> _AuthRequiredActionsHandler:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_AuthRequiredActionsHandler: The dictionary representation suitable for internal use.
		"""
		
		return _AuthRequiredActionsHandler(
				choose_action_func=self.choose_action_func,
				actions=self.actions.to_dict()
				if self.actions is not None
				else AuthRequiredActionsSettings().to_dict(),
		)


class _AuthRequired(AbstractEvent):
	"""
	Internal TypedDict representing the complete configuration for an 'AuthRequired' event listener.

	This structure extends `AbstractEvent` with specifics for the Fetch.AuthRequired domain event.

	Attributes:
		class_to_use_path (str): Path to the CDP event class ("fetch.AuthRequired").
		listen_buffer_size (int): Buffer size for the listener channel.
		handle_function (handle_auth_required_func_type): The main handler function for the event (_handle_auth_required).
		actions_handler (_AuthRequiredActionsHandler): Callbacks and configurations for choosing and executing actions based on the event.
		on_error_func (on_error_func_type): Function to call on error during event handling.
	"""
	
	class_to_use_path: str
	listen_buffer_size: int
	handle_function: "handle_auth_required_func_type"
	actions_handler: _AuthRequiredActionsHandler
	on_error_func: on_error_func_type


async def _handle_auth_required(self: "DevToolsTarget", handler_settings: _AuthRequired, event: Any):
	"""
	Handles the 'fetch.AuthRequired' CDP event.

	This function determines which actions to take based on the `choose_action_func`
	defined in the handler settings, builds the necessary keyword arguments for the
	chosen actions using their respective parameter handlers, executes the CDP commands,
	and processes their responses.

	Args:
		self (DevToolsTarget): The DevToolsTarget instance.
		handler_settings (_AuthRequired): The configuration settings for handling the 'AuthRequired' event.
		event (Any): The 'AuthRequired' event object received from the CDP.

	Raises:
		BaseException: If a critical error occurs during the event handling process.
	"""
	
	await self.log(level="INFO", message=f"Started to handle for '{event}'")
	
	try:
		chosen_actions_func_names = handler_settings["actions_handler"]["choose_action_func"](self, event)
		await self.log(level="INFO", message=f"Chosen actions: '{chosen_actions_func_names}'")
	
		for action_func_name in chosen_actions_func_names:
			chosen_func = handler_settings["actions_handler"]["actions"][action_func_name]
			kwargs = await chosen_func["kwargs_func"](self, chosen_func["parameters_handlers"], event)
			await self.log(level="INFO", message=f"Kwargs for '{action_func_name}': '{kwargs}'")
			response_handle_func = chosen_func["response_handle_func"]
	
			try:
				response = await execute_cdp_command(
						self,
						"raise",
						await self.get_devtools_object(f"fetch.{action_func_name}"),
						**kwargs
				)
				await self.log(
						level="AuthRequired",
						message=f"Function '{action_func_name}' response: '{response}'"
				)
	
				if response_handle_func is not None:
					self._nursery_object.start_soon(response_handle_func, self, response)
			except* cdp_end_exceptions:
				pass
			except* BaseException as error:
				await self.log_error(error=error)
	
				on_error = handler_settings["on_error_func"]
	
				if on_error is not None:
					on_error(self, event, error)
	except* cdp_end_exceptions as error:
		raise error
	except* BaseException as error:
		await self.log_error(error=error)
		raise error


@dataclass
class AuthRequiredSettings(AbstractEventSettings):
	"""
	Settings for handling the 'fetch.AuthRequired' event.

	This dataclass allows configuring the listener for the 'AuthRequired' CDP event,
	including buffer size, the actions to take, and error handling.

	Attributes:
		actions_handler (AuthRequiredActionsHandlerSettings): Configuration for the event's actions handler, determining which action to take (e.g., continueWithAuth) and how to build its parameters.
		listen_buffer_size (int): The buffer size for the event listener channel. Defaults to 10.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling. Defaults to None.
	"""
	
	actions_handler: AuthRequiredActionsHandlerSettings
	listen_buffer_size: int = 10
	on_error_func: on_error_func_type = None
	
	@property
	def handle_function(self) -> "handle_auth_required_func_type":
		"""
		Returns the main handler function for the 'fetch.AuthRequired' event.

		Returns:
			handle_auth_required_func_type: The internal function `_handle_auth_required`.
		"""
		
		return _handle_auth_required
	
	@property
	def class_to_use_path(self) -> str:
		"""
		Returns the path to the CDP event class for 'fetch.AuthRequired'.

		Returns:
			str: The string "fetch.AuthRequired".
		"""
		
		return "fetch.AuthRequired"
	
	def to_dict(self) -> _AuthRequired:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_AuthRequired: The dictionary representation suitable for internal use.
		"""
		
		return _AuthRequired(
				class_to_use_path=self.class_to_use_path,
				listen_buffer_size=self.listen_buffer_size,
				handle_function=self.handle_function,
				actions_handler=self.actions_handler.to_dict(),
				on_error_func=self.on_error_func,
		)


class _ContinueResponseParametersHandlers(TypedDict):
	"""
	Internal TypedDict for handlers related to the 'continueResponse' action parameters.

	Attributes:
		response_code (Optional[ParameterHandler]): Handler for the HTTP response code.
		response_phrase (Optional[ParameterHandler]): Handler for the HTTP response phrase.
		response_headers (Optional[ParameterHandler]): Handler for the response headers.
		binary_response_headers (Optional[ParameterHandler]): Handler for binary response headers (base64 encoded).
	"""
	
	response_code: Optional[ParameterHandler]
	response_phrase: Optional[ParameterHandler]
	response_headers: Optional[ParameterHandler]
	binary_response_headers: Optional[ParameterHandler]


class _ContinueResponseAction(AbstractAction):
	"""
	Internal TypedDict for the 'continueResponse' action configuration within RequestPaused.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the `continueResponse` CDP command.
		response_handle_func (response_handle_func_type): A function to process the response from the CDP command.
		parameters_handlers (_ContinueResponseParametersHandlers): Handlers for modifying response parameters.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type
	response_handle_func: response_handle_func_type
	parameters_handlers: _ContinueResponseParametersHandlers


class _FulfillRequestParametersHandlers(TypedDict):
	"""
	Internal TypedDict for handlers related to the 'fulfillRequest' action parameters.

	Attributes:
		response_code (ParameterHandler): Required handler for the HTTP response code (e.g., 200).
		response_headers (Optional[ParameterHandler]): Handler for the response headers.
		binary_response_headers (Optional[ParameterHandler]): Handler for binary response headers (base64 encoded).
		body (Optional[ParameterHandler]): Handler for the response body (base64 encoded string).
		response_phrase (Optional[ParameterHandler]): Handler for the HTTP response phrase (e.g., "OK").
	"""
	
	response_code: ParameterHandler
	response_headers: Optional[ParameterHandler]
	binary_response_headers: Optional[ParameterHandler]
	body: Optional[ParameterHandler]
	response_phrase: Optional[ParameterHandler]


class _FulfillRequestAction(AbstractAction):
	"""
	Internal TypedDict for the 'fulfillRequest' action configuration within RequestPaused.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the `fulfillRequest` CDP command.
		response_handle_func (response_handle_func_type): A function to process the response from the CDP command.
		parameters_handlers (_FulfillRequestParametersHandlers): Handlers for mock response parameters.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type
	response_handle_func: response_handle_func_type
	parameters_handlers: _FulfillRequestParametersHandlers


class _FailRequestParametersHandlers(TypedDict):
	"""
	Internal TypedDict for handlers related to the 'failRequest' action parameters.

	Attributes:
		error_reason (ParameterHandler): Required handler for providing the network error reason (a string from Network.ErrorReason enum).
	"""
	
	error_reason: ParameterHandler


class _FailRequestAction(AbstractAction):
	"""
	Internal TypedDict for the 'failRequest' action configuration within RequestPaused.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the `failRequest` CDP command.
		response_handle_func (response_handle_func_type): A function to process the response from the CDP command.
		parameters_handlers (_FailRequestParametersHandlers): Handlers for the error reason parameter.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type
	response_handle_func: response_handle_func_type
	parameters_handlers: _FailRequestParametersHandlers


class _ContinueRequestParametersHandlers(TypedDict):
	"""
	Internal TypedDict for handlers related to the 'continueRequest' action parameters.

	Attributes:
		url (Optional[ParameterHandler]): Handler for modifying the request URL.
		method (Optional[ParameterHandler]): Handler for modifying the HTTP method.
		post_data (Optional[ParameterHandler]): Handler for modifying the request's post data (base64 encoded string).
		headers (Optional[ParameterHandler]): Handler for modifying the request headers.
		intercept_response (Optional[ParameterHandler]): Handler for setting response interception behavior for this request.
	"""
	
	url: Optional[ParameterHandler]
	method: Optional[ParameterHandler]
	post_data: Optional[ParameterHandler]
	headers: Optional[ParameterHandler]
	intercept_response: Optional[ParameterHandler]


class _ContinueRequestAction(AbstractAction):
	"""
	Internal TypedDict for the 'continueRequest' action configuration within RequestPaused.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the `continueRequest` CDP command.
		response_handle_func (response_handle_func_type): A function to process the response from the CDP command.
		parameters_handlers (_ContinueRequestParametersHandlers): Handlers for modifying request parameters.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type
	response_handle_func: response_handle_func_type
	parameters_handlers: _ContinueRequestParametersHandlers


class _RequestPausedActions(TypedDict):
	"""
	Internal TypedDict mapping action names for RequestPaused event to their configurations.

	Attributes:
		continue_request (Optional[_ContinueRequestAction]): Configuration for the 'continueRequest' action.
		fail_request (Optional[_FailRequestAction]): Configuration for the 'failRequest' action.
		fulfill_request (Optional[_FulfillRequestAction]): Configuration for the 'fulfillRequest' action.
		continue_response (Optional[_ContinueResponseAction]): Configuration for the 'continueResponse' action.
	"""
	
	continue_request: Optional[_ContinueRequestAction]
	fail_request: Optional[_FailRequestAction]
	fulfill_request: Optional[_FulfillRequestAction]
	continue_response: Optional[_ContinueResponseAction]


class _RequestPausedActionsHandler(AbstractEventActionsHandler):
	"""
	Internal TypedDict for the actions handler configuration for the 'RequestPaused' event.

	Attributes:
		choose_action_func (request_paused_choose_action_func_type): A function that determines which actions (by name) should be executed for a given 'RequestPaused' event.
		actions (_RequestPausedActions): A dictionary mapping action names to their full configurations.
	"""
	
	choose_action_func: "request_paused_choose_action_func_type"
	actions: _RequestPausedActions


class _RequestPaused(AbstractEvent):
	"""
	Internal TypedDict representing the complete configuration for a 'RequestPaused' event listener.

	This structure extends `AbstractEvent` with specifics for the Fetch.RequestPaused domain event.

	Attributes:
		class_to_use_path (str): Path to the CDP event class ("fetch.RequestPaused").
		listen_buffer_size (int): Buffer size for the listener channel.
		handle_function (handle_request_paused_func_type): The main handler function for the event (_handle_request_paused).
		actions_handler (_RequestPausedActionsHandler): Callbacks and configurations for choosing and executing actions based on the event.
		on_error_func (on_error_func_type): Function to call on error during event handling.
	"""
	
	class_to_use_path: str
	listen_buffer_size: int
	handle_function: "handle_request_paused_func_type"
	actions_handler: _RequestPausedActionsHandler
	on_error_func: on_error_func_type


async def _handle_request_paused(self: "DevToolsTarget", handler_settings: _RequestPaused, event: Any):
	"""
	Handles the 'fetch.RequestPaused' CDP event.

	This function determines which actions to take based on the `choose_action_func`
	defined in the handler settings, builds the necessary keyword arguments for the
	chosen actions using their respective parameter handlers, executes the CDP commands,
	and processes their responses.

	Args:
		self (DevToolsTarget): The DevToolsTarget instance.
		handler_settings (_RequestPaused): The configuration settings for handling the 'RequestPaused' event.
		event (Any): The 'RequestPaused' event object received from the CDP.

	Raises:
		BaseException: If a critical error occurs during the event handling process.
	"""
	
	await self.log(level="INFO", message=f"Started to handle for '{event}'")
	
	try:
		chosen_actions_func_names = handler_settings["actions_handler"]["choose_action_func"](self, event)
		await self.log(level="INFO", message=f"Chosen actions: '{chosen_actions_func_names}'")
	
		for action_func_name in chosen_actions_func_names:
			chosen_action_func = handler_settings["actions_handler"]["actions"][action_func_name]
	
			kwargs = await chosen_action_func["kwargs_func"](self, chosen_action_func["parameters_handlers"], event)
			await self.log(level="INFO", message=f"Kwargs for '{action_func_name}': '{kwargs}'")
	
			response_handle_func = chosen_action_func["response_handle_func"]
	
			try:
				response = await execute_cdp_command(
						self,
						"raise",
						await self.get_devtools_object(f"fetch.{action_func_name}"),
						**kwargs
				)
				await self.log(
						level="RequestPaused",
						message=f"Function '{action_func_name}' response: '{response}'"
				)
	
				if response_handle_func is not None:
					self._nursery_object.start_soon(response_handle_func, self, response)
			except* cdp_end_exceptions:
				pass
			except* BaseException as error:
				await self.log_error(error=error)
	
				on_error = handler_settings["on_error_func"]
	
				if on_error is not None:
					on_error(self, event, error)
	except* cdp_end_exceptions as error:
		raise error
	except* BaseException as error:
		await self.log_error(error=error)
		raise error


@dataclass
class ContinueResponseHandlersSettings(AbstractActionParametersHandlersSettings):
	"""
	Configuration for handlers that modify a response before it continues using `fetch.continueResponse`.

	These handlers provide parameter values for the `fetch.continueResponse` CDP command.

	Attributes:
		response_code (Optional[ParameterHandler]): Handler for the HTTP response code. Defaults to None.
		response_phrase (Optional[ParameterHandler]): Handler for the HTTP response phrase. Defaults to None.
		response_headers (Optional[ParameterHandler]): Handler for the response headers. Defaults to None.
		binary_response_headers (Optional[ParameterHandler]): Handler for binary response headers (base64 encoded). Defaults to None.
	"""
	
	response_code: Optional[ParameterHandler] = None
	response_phrase: Optional[ParameterHandler] = None
	response_headers: Optional[ParameterHandler] = None
	binary_response_headers: Optional[ParameterHandler] = None
	
	def to_dict(self) -> _ContinueResponseParametersHandlers:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_ContinueResponseParametersHandlers: The dictionary representation suitable for internal use.
		"""
		
		return _ContinueResponseParametersHandlers(
				response_code=self.response_code,
				response_phrase=self.response_phrase,
				response_headers=self.response_headers,
				binary_response_headers=self.binary_response_headers
		)


@dataclass
class ContinueResponseSettings(AbstractActionSettings):
	"""
	Settings for the 'continueResponse' action for a paused request (from RequestPaused event).

	This action is used to modify and continue a request *after* the response has been received but before it is processed by the browser.

	Attributes:
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.continueResponse` CDP command. Defaults to None.
		parameters_handlers (Optional[ContinueResponseHandlersSettings]): Configuration for the response parameter handlers that provide modified response details. Defaults to None.
	"""
	
	response_handle_func: response_handle_func_type = None
	parameters_handlers: Optional[ContinueResponseHandlersSettings] = None
	
	@property
	def kwargs_func(self) -> build_kwargs_from_handlers_func_type:
		"""
		Returns the function used to build keyword arguments for the `continueResponse` command.

		Returns:
			build_kwargs_from_handlers_func_type: The internal function `_build_kwargs_from_handlers_func`.
		"""
		
		return _build_kwargs_from_handlers_func
	
	def to_dict(self) -> _ContinueResponseAction:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_ContinueResponseAction: The dictionary representation suitable for internal use.
		"""
		
		return _ContinueResponseAction(
				kwargs_func=self.kwargs_func,
				response_handle_func=self.response_handle_func,
				parameters_handlers=self.parameters_handlers.to_dict()
				if self.parameters_handlers is not None
				else ContinueResponseHandlersSettings().to_dict(),
		)


@dataclass
class FulfillRequestHandlersSettings(AbstractActionParametersHandlersSettings):
	"""
	Configuration for handlers that provide a mock response to a request using `fetch.fulfillRequest`.

	These handlers provide parameter values for the `fetch.fulfillRequest` CDP command.

	Attributes:
		response_code (ParameterHandler): Required handler for the HTTP response code (e.g., 200).
		response_headers (Optional[ParameterHandler]): Handler for the response headers. Defaults to None.
		binary_response_headers (Optional[ParameterHandler]): Handler for binary response headers (base64 encoded). Defaults to None.
		body (Optional[ParameterHandler]): Handler for the response body (base64 encoded string). Defaults to None.
		response_phrase (Optional[ParameterHandler]): Handler for the HTTP response phrase (e.g., "OK"). Defaults to None.
	"""
	
	response_code: ParameterHandler
	response_headers: Optional[ParameterHandler] = None
	binary_response_headers: Optional[ParameterHandler] = None
	body: Optional[ParameterHandler] = None
	response_phrase: Optional[ParameterHandler] = None
	
	def to_dict(self) -> _FulfillRequestParametersHandlers:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_FulfillRequestParametersHandlers: The dictionary representation suitable for internal use.
		"""
		
		return _FulfillRequestParametersHandlers(
				response_code=self.response_code,
				response_headers=self.response_headers,
				binary_response_headers=self.binary_response_headers,
				body=self.body,
				response_phrase=self.response_phrase,
		)


@dataclass
class FulfillRequestSettings(AbstractActionSettings):
	"""
	Settings for the 'fulfillRequest' action for a paused request (from RequestPaused event).

	This action is used to provide a completely mock response for a request, preventing the browser from sending it to the network.

	Attributes:
		parameters_handlers (FulfillRequestHandlersSettings): Configuration for the mock response parameter handlers.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.fulfillRequest` CDP command. Defaults to None.
	"""
	
	parameters_handlers: FulfillRequestHandlersSettings
	response_handle_func: response_handle_func_type = None
	
	@property
	def kwargs_func(self) -> build_kwargs_from_handlers_func_type:
		"""
		Returns the function used to build keyword arguments for the `fulfillRequest` command.

		Returns:
			build_kwargs_from_handlers_func_type: The internal function `_build_kwargs_from_handlers_func`.
		"""
		
		return _build_kwargs_from_handlers_func
	
	def to_dict(self) -> _FulfillRequestAction:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_FulfillRequestAction: The dictionary representation suitable for internal use.
		"""
		
		return _FulfillRequestAction(
				kwargs_func=self.kwargs_func,
				response_handle_func=self.response_handle_func,
				parameters_handlers=self.parameters_handlers.to_dict(),
		)


@dataclass
class FailRequestHandlersSettings(AbstractActionParametersHandlersSettings):
	"""
	Configuration for handlers that specify the reason for failing a request using `fetch.failRequest`.

	These handlers provide parameter values for the `fetch.failRequest` CDP command.

	Attributes:
		error_reason (ParameterHandler): Required handler for providing the network error reason (a string from Network.ErrorReason enum, e.g., "Aborted", "AccessDenied").
	"""
	
	error_reason: ParameterHandler
	
	def to_dict(self) -> _FailRequestParametersHandlers:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_FailRequestParametersHandlers: The dictionary representation suitable for internal use.
		"""
		
		return _FailRequestParametersHandlers(error_reason=self.error_reason)


@dataclass
class FailRequestSettings(AbstractActionSettings):
	"""
	Settings for the 'failRequest' action for a paused request (from RequestPaused event).

	This action is used to cause the request to fail with a specific network error reason.

	Attributes:
		parameters_handlers (FailRequestHandlersSettings): Configuration for the error reason handler.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.failRequest` CDP command. Defaults to None.
	"""
	
	parameters_handlers: FailRequestHandlersSettings
	response_handle_func: response_handle_func_type = None
	
	@property
	def kwargs_func(self) -> build_kwargs_from_handlers_func_type:
		"""
		Returns the function used to build keyword arguments for the `failRequest` command.

		Returns:
			build_kwargs_from_handlers_func_type: The internal function `_build_kwargs_from_handlers_func`.
		"""
		
		return _build_kwargs_from_handlers_func
	
	def to_dict(self) -> _FailRequestAction:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_FailRequestAction: The dictionary representation suitable for internal use.
		"""
		
		return _FailRequestAction(
				kwargs_func=self.kwargs_func,
				response_handle_func=self.response_handle_func,
				parameters_handlers=self.parameters_handlers.to_dict(),
		)


@dataclass
class ContinueRequestHandlersSettings(AbstractActionParametersHandlersSettings):
	"""
	Configuration for handlers that modify a request before it continues using `fetch.continueRequest`.

	These handlers provide parameter values for the `fetch.continueRequest` CDP command.

	Attributes:
		url (Optional[ParameterHandler]): Handler for modifying the request URL. Defaults to None.
		method (Optional[ParameterHandler]): Handler for modifying the HTTP method. Defaults to None.
		post_data (Optional[ParameterHandler]): Handler for modifying the request's post data (base64 encoded string). Defaults to None.
		headers (Optional[ParameterHandler]): Handler for modifying the request headers. Defaults to None.
		intercept_response (Optional[ParameterHandler]): Handler for setting response interception behavior for this request. Defaults to None.
	"""
	
	url: Optional[ParameterHandler] = None
	method: Optional[ParameterHandler] = None
	post_data: Optional[ParameterHandler] = None
	headers: Optional[ParameterHandler] = None
	intercept_response: Optional[ParameterHandler] = None
	
	def to_dict(self) -> _ContinueRequestParametersHandlers:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_ContinueRequestParametersHandlers: The dictionary representation suitable for internal use.
		"""
		
		return _ContinueRequestParametersHandlers(
				url=self.url,
				method=self.method,
				post_data=self.post_data,
				headers=self.headers,
				intercept_response=self.intercept_response,
		)


@dataclass
class ContinueRequestSettings(AbstractActionSettings):
	"""
	Settings for the 'continueRequest' action for a paused request (from RequestPaused event).

	This action is used to allow the request to proceed, optionally after modifying it.

	Attributes:
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.continueRequest` CDP command. Defaults to None.
		parameters_handlers (Optional[ContinueRequestHandlersSettings]): Configuration for the request parameter handlers that provide modified request details. Defaults to None.
	"""
	
	response_handle_func: response_handle_func_type = None
	parameters_handlers: Optional[ContinueRequestHandlersSettings] = None
	
	@property
	def kwargs_func(self) -> build_kwargs_from_handlers_func_type:
		"""
		Returns the function used to build keyword arguments for the `continueRequest` command.

		Returns:
			build_kwargs_from_handlers_func_type: The internal function `_build_kwargs_from_handlers_func`.
		"""
		
		return _build_kwargs_from_handlers_func
	
	def to_dict(self) -> _ContinueRequestAction:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_ContinueRequestAction: The dictionary representation suitable for internal use.
		"""
		
		return _ContinueRequestAction(
				kwargs_func=self.kwargs_func,
				response_handle_func=self.response_handle_func,
				parameters_handlers=self.parameters_handlers.to_dict()
				if self.parameters_handlers is not None
				else ContinueRequestHandlersSettings().to_dict(),
		)


@dataclass
class RequestPausedActionsSettings(AbstractEventActionsSettings):
	"""
	Container for configurations of possible actions to take when a request is paused.

	Attributes:
		continue_request (Optional[ContinueRequestSettings]): Settings for handling the paused request using `fetch.continueRequest`. Defaults to None.
		fail_request (Optional[FailRequestSettings]): Settings for handling the paused request using `fetch.failRequest`. Defaults to None.
		fulfill_request (Optional[FulfillRequestSettings]): Settings for handling the paused request using `fetch.fulfillRequest`. Defaults to None.
		continue_response (Optional[ContinueResponseSettings]): Settings for handling the paused request using `fetch.continueResponse`. Defaults to None.
	"""
	
	continue_request: Optional[ContinueRequestSettings] = None
	fail_request: Optional[FailRequestSettings] = None
	fulfill_request: Optional[FulfillRequestSettings] = None
	continue_response: Optional[ContinueResponseSettings] = None
	
	def to_dict(self) -> _RequestPausedActions:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_RequestPausedActions: The dictionary representation suitable for internal use.
		"""
		
		return _RequestPausedActions(
				continue_request=self.continue_request.to_dict()
				if self.continue_request
				else None,
				fail_request=self.fail_request.to_dict()
				if self.fail_request
				else None,
				fulfill_request=self.fulfill_request.to_dict()
				if self.fulfill_request
				else None,
				continue_response=self.continue_response.to_dict()
				if self.continue_response
				else None,
		)


@dataclass
class RequestPausedActionsHandlerSettings(AbstractEventActionsHandlerSettings):
	"""
	Settings for handling the 'fetch.RequestPaused' event by choosing and executing specific actions.

	Attributes:
		choose_action_func (request_paused_choose_action_func_type): A function that takes the DevTools instance and the event object and returns a list of action names (Literals) to execute. Defaults to `request_paused_choose_func`.
		actions (Optional[RequestPausedActionsSettings]): Container for the configuration of the available actions. Defaults to None.
	"""
	
	choose_action_func: "request_paused_choose_action_func_type" = request_paused_choose_func
	actions: Optional[RequestPausedActionsSettings] = None
	
	def to_dict(self) -> _RequestPausedActionsHandler:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_RequestPausedActionsHandler: The dictionary representation suitable for internal use.
		"""
		
		return _RequestPausedActionsHandler(
				choose_action_func=self.choose_action_func,
				actions=self.actions.to_dict()
				if self.actions is not None
				else RequestPausedActionsSettings().to_dict(),
		)


@dataclass
class RequestPausedSettings(AbstractEventSettings):
	"""
	Settings for handling the 'fetch.RequestPaused' event.

	This dataclass allows configuring the listener for the 'RequestPaused' CDP event,
	including buffer size, the actions to take, and error handling.

	Attributes:
		listen_buffer_size (int): The buffer size for the event listener channel. Defaults to 100.
		actions_handler (Optional[RequestPausedActionsHandlerSettings]): Configuration for the event's actions handler, determining which action(s) to take (e.g., continueRequest, fulfillRequest) and how to build their parameters. Defaults to None.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling. Defaults to None.
	"""
	
	listen_buffer_size: int = 100
	actions_handler: Optional[RequestPausedActionsHandlerSettings] = None
	on_error_func: on_error_func_type = None
	
	@property
	def handle_function(self) -> "handle_request_paused_func_type":
		"""
		Returns the main handler function for the 'fetch.RequestPaused' event.

		Returns:
			handle_request_paused_func_type: The internal function `_handle_request_paused`.
		"""
		
		return _handle_request_paused
	
	@property
	def class_to_use_path(self) -> str:
		"""
		Returns the path to the CDP event class for 'fetch.RequestPaused'.

		Returns:
			str: The string "fetch.RequestPaused".
		"""
		
		return "fetch.RequestPaused"
	
	def to_dict(self) -> _RequestPaused:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_RequestPaused: The dictionary representation suitable for internal use.
		"""
		
		return _RequestPaused(
				class_to_use_path=self.class_to_use_path,
				listen_buffer_size=self.listen_buffer_size,
				handle_function=self.handle_function,
				actions_handler=self.actions_handler.to_dict()
				if self.actions_handler is not None
				else RequestPausedActionsHandlerSettings().to_dict(),
				on_error_func=self.on_error_func,
		)


class _FetchHandlers(TypedDict):
	"""
	Internal TypedDict for all event handlers within the Fetch domain.

	Attributes:
		request_paused (Optional[_RequestPaused]): Configuration for the 'RequestPaused' event handler.
		auth_required (Optional[_AuthRequired]): Configuration for the 'AuthRequired' event handler.
	"""
	
	request_paused: Optional[_RequestPaused]
	auth_required: Optional[_AuthRequired]


@dataclass
class FetchHandlersSettings(AbstractDomainHandlersSettings):
	"""
	Container for all handler settings within the Fetch domain.

	Attributes:
		request_paused (Optional[RequestPausedSettings]): Settings for the 'RequestPaused' event handler. Defaults to None.
		auth_required (Optional[AuthRequiredSettings]): Settings for the 'AuthRequired' event handler. Defaults to None.
	"""
	
	request_paused: Optional[RequestPausedSettings] = None
	auth_required: Optional[AuthRequiredSettings] = None
	
	def to_dict(self) -> _FetchHandlers:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_FetchHandlers: The dictionary representation suitable for internal use.
		"""
		
		return _FetchHandlers(
				request_paused=self.request_paused.to_dict()
				if self.request_paused is not None
				else None,
				auth_required=self.auth_required.to_dict()
				if self.auth_required is not None
				else None,
		)


class _FetchEnableKwargs(TypedDict, total=False):
	"""
	Internal TypedDict for keyword arguments to enable the Fetch domain.

	Attributes:
		patterns (Optional[Sequence[Any]]): A list of request patterns to intercept.
		handle_auth_requests (Optional[bool]): Whether to intercept authentication requests.
	"""
	
	patterns: Optional[Sequence[Any]]
	handle_auth_requests: Optional[bool]


@dataclass
class FetchEnableKwargsSettings(AbstractDomainEnableKwargsSettings):
	"""
	Keyword arguments for enabling the Fetch domain using `fetch.enable`.

	These settings are passed to the `fetch.enable` CDP command when the Fetch domain is activated.

	Attributes:
		patterns (Optional[Sequence[Any]]): A list of request patterns to intercept. Each pattern is typically a dictionary matching the CDP `Fetch.RequestPattern` type. If None, all requests are intercepted. Defaults to None.
		handle_auth_requests (Optional[bool]): Whether to intercept authentication requests (`fetch.AuthRequired` events). If True, `auth_required` events will be emitted. Defaults to None.
	"""
	
	patterns: Optional[Sequence[Any]] = None
	handle_auth_requests: Optional[bool] = None
	
	def to_dict(self) -> _FetchEnableKwargs:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_FetchEnableKwargs: The dictionary representation suitable for internal use.
		"""
		
		kwargs = {}
		
		if self.patterns is not None:
			kwargs["patterns"] = self.patterns
		
		if self.handle_auth_requests is not None:
			kwargs["handle_auth_requests"] = self.handle_auth_requests
		
		return _FetchEnableKwargs(**kwargs)


class _Fetch(AbstractDomain):
	"""
	Internal TypedDict for the complete Fetch domain configuration.

	This structure is used internally by the DevTools manager to configure the
	Fetch domain, including how to enable/disable it and what event handlers to use.

	Attributes:
		name (str): The name of the domain ('fetch').
		enable_func_path (str): The path to the function to enable the domain ("fetch.enable").
		enable_func_kwargs (Optional[_FetchEnableKwargs]): Keyword arguments for the enable function.
		disable_func_path (str): The path to the function to disable the domain ("fetch.disable").
		handlers (_FetchHandlers): The configured event handlers for the domain.
	"""
	
	name: str
	enable_func_path: str
	enable_func_kwargs: Optional[_FetchEnableKwargs]
	disable_func_path: str
	handlers: _FetchHandlers


@dataclass
class FetchSettings(AbstractDomainSettings):
	"""
	Top-level configuration for the Fetch domain.

	This dataclass allows configuring the entire Fetch CDP domain within the DevTools manager,
	including its enabling parameters and event handlers.

	Attributes:
		enable_func_kwargs (Optional[FetchEnableKwargsSettings]): Keyword arguments for enabling the Fetch domain using `fetch.enable`. Defaults to None.
		handlers (FetchHandlersSettings): Container for all handler settings within the Fetch domain (e.g., RequestPaused, AuthRequired). Defaults to None.
	"""
	
	enable_func_kwargs: Optional[FetchEnableKwargsSettings] = None
	handlers: Optional[FetchHandlersSettings] = None
	
	@property
	def disable_func_path(self) -> str:
		"""
		Returns the path to the function to disable the domain.

		Returns:
			str: The string "fetch.disable".
		"""
		
		return "fetch.disable"
	
	@property
	def enable_func_path(self) -> str:
		"""
		Returns the path to the function to enable the domain.

		Returns:
			str: The string "fetch.enable".
		"""
		
		return "fetch.enable"
	
	@property
	def name(self) -> str:
		"""
		Returns the name of the domain.

		Returns:
			str: The string "fetch".
		"""
		
		return "fetch"
	
	def to_dict(self) -> _Fetch:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			_Fetch: The dictionary representation suitable for internal use.
		"""
		
		return _Fetch(
				name=self.name,
				enable_func_path=self.enable_func_path,
				enable_func_kwargs=self.enable_func_kwargs.to_dict()
				if self.enable_func_kwargs is not None
				else FetchEnableKwargsSettings().to_dict(),
				disable_func_path=self.disable_func_path,
				handlers=self.handlers.to_dict()
				if self.handlers is not None
				else FetchHandlersSettings().to_dict(),
		)


request_paused_actions_literal = Literal[
	"continue_request",
	"fail_request",
	"fulfill_request",
	"continue_response"
]
auth_required_actions_literal = Literal["continue_with_auth"]
request_paused_choose_action_func_type = Callable[["DevToolsTarget", Any], Sequence[request_paused_actions_literal]]
auth_required_choose_action_func_type = Callable[["DevToolsTarget", Any], Sequence[auth_required_actions_literal]]
handle_request_paused_func_type = Callable[["DevToolsTarget", _RequestPaused, Any], Awaitable[None]]
handle_auth_required_func_type = Callable[["DevToolsTarget", _AuthRequired, Any], Awaitable[None]]
