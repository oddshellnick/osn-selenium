import trio
from pydantic import Field
from osn_selenium._base_models import DictModel
from osn_selenium.dev_tools._functions import execute_cdp_command
from osn_selenium.exceptions.devtools import (
	CDPEndExceptions,
	ExceptionThrown
)
from typing import (
	Any,
	Callable,
	Coroutine,
	List,
	Literal,
	Mapping,
	Optional,
	Sequence,
	TYPE_CHECKING
)
from osn_selenium.dev_tools.domains_default.fetch import (
	auth_required_choose_func,
	request_paused_choose_func
)
from osn_selenium.dev_tools.domains.abstract import (
	AbstractActionParametersHandlersSettings,
	AbstractActionSettings,
	AbstractDomainEnableKwargsSettings,
	AbstractDomainHandlersSettings,
	AbstractDomainSettings,
	AbstractEventActionsHandlerSettings,
	AbstractEventActionsSettings,
	AbstractEventSettings,
	ParameterHandler,
	build_kwargs_from_handlers_func_type,
	kwargs_type,
	on_error_func_type,
	response_handle_func_type
)


__all__ = [
	"AuthRequiredActionsHandlerSettings",
	"AuthRequiredActionsSettings",
	"AuthRequiredSettings",
	"ContinueRequestHandlersSettings",
	"ContinueRequestSettings",
	"ContinueResponseHandlersSettings",
	"ContinueResponseSettings",
	"ContinueWithAuthParameterHandlersSettings",
	"ContinueWithAuthSettings",
	"FailRequestHandlersSettings",
	"FailRequestSettings",
	"FetchEnableKwargsSettings",
	"FetchHandlersSettings",
	"FetchSettings",
	"FulfillRequestHandlersSettings",
	"FulfillRequestSettings",
	"RequestPausedActionsHandlerSettings",
	"RequestPausedActionsSettings",
	"RequestPausedSettings",
	"auth_required_actions_literal",
	"auth_required_choose_action_func_type",
	"handle_auth_required_func_type",
	"handle_request_paused_func_type",
	"request_paused_actions_literal",
	"request_paused_choose_action_func_type"
]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target import DevToolsTarget
else:
	DevToolsTarget = Any

request_paused_actions_literal = Literal[
	"continue_request",
	"fail_request",
	"fulfill_request",
	"continue_response"
]
auth_required_actions_literal = Literal["continue_with_auth"]

request_paused_choose_action_func_type = Callable[[DevToolsTarget, Any], Sequence[request_paused_actions_literal]]
handle_request_paused_func_type = Callable[[DevToolsTarget, "RequestPausedSettings", Any], Coroutine[Any, Any, None]]

auth_required_choose_action_func_type = Callable[[DevToolsTarget, Any], Sequence[auth_required_actions_literal]]
handle_auth_required_func_type = Callable[[DevToolsTarget, "AuthRequiredSettings", Any], Coroutine[Any, Any, None]]


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


async def _build_kwargs_from_handlers_func(self: DevToolsTarget, handlers: DictModel, event: Any) -> kwargs_type:
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
	
	await self.log_cdp(level="INFO", message=f"Started to build kwargs for '{event}'")
	
	try:
		kwargs = {"request_id": event.request_id}
	
		kwargs_ready_events: List[trio.Event] = []
	
		for handler_name, handler_settings in handlers:
			if handler_settings is not None:
				kwargs_ready_event = trio.Event()
				kwargs_ready_events.append(kwargs_ready_event)
	
				self._nursery_object.start_soon(
						handler_settings.func,
						self,
						kwargs_ready_event,
						handler_settings.instances,
						event,
						kwargs
				)
	
		for kwargs_ready_event in kwargs_ready_events:
			await kwargs_ready_event.wait()
	
		return kwargs
	except* CDPEndExceptions as error:
		raise error
	except* BaseException as error:
		await self.log_cdp_error(error=error)
		raise error


class ContinueWithAuthSettings(AbstractActionSettings):
	"""
	Settings for continuing a request that requires authentication using the `fetch.continueWithAuth` CDP command.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments from handlers. Defaults to internal builder.
		parameters_handlers (ContinueWithAuthParameterHandlersSettings): Settings for the handlers that provide authentication credentials.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.continueWithAuth` CDP command. Defaults to None.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type = _build_kwargs_from_handlers_func
	parameters_handlers: ContinueWithAuthParameterHandlersSettings
	response_handle_func: response_handle_func_type = None


class AuthRequiredActionsSettings(AbstractEventActionsSettings):
	"""
	Container for configurations of possible actions to take when authentication is required.

	Attributes:
		continue_with_auth (Optional[ContinueWithAuthSettings]): Settings for handling the authentication challenge using `fetch.continueWithAuth`. Defaults to None.
	"""
	
	continue_with_auth: Optional[ContinueWithAuthSettings] = None


class AuthRequiredActionsHandlerSettings(AbstractEventActionsHandlerSettings):
	"""
	Settings for handling the 'fetch.AuthRequired' event by choosing and executing specific actions.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Helper function for keyword argument building. Defaults to internal builder.
		choose_action_func (auth_required_choose_action_func_type): A function that takes the DevTools instance and the event object and returns a List of action names (Literals) to execute. Defaults to `auth_required_choose_func`.
		actions (Optional[AuthRequiredActionsSettings]): Container for the configuration of the available actions. Defaults to None.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type = _build_kwargs_from_handlers_func
	choose_action_func: auth_required_choose_action_func_type = auth_required_choose_func
	actions: Optional[AuthRequiredActionsSettings] = None


async def _handle_auth_required(
		self: DevToolsTarget,
		handler_settings: "AuthRequiredSettings",
		event: Any
):
	"""
	Handles the 'fetch.AuthRequired' CDP event.

	This function determines which actions to take based on the `choose_action_func`
	defined in the handler settings, builds the necessary keyword arguments for the
	chosen actions using their respective parameter handlers, executes the CDP commands,
	and processes their responses.

	Args:
		self (DevToolsTarget): The DevToolsTarget instance.
		handler_settings (AuthRequiredSettings): The configuration settings for handling the 'AuthRequired' event.
		event (Any): The 'AuthRequired' event object received from the CDP.

	Raises:
		BaseException: If a critical error occurs during the event handling process.
	"""
	
	await self.log_cdp(level="INFO", message=f"Started to handle for '{event}'")
	
	try:
		chosen_actions_func_names = handler_settings.actions_handler.choose_action_func(self, event)
		await self.log_cdp(level="INFO", message=f"Chosen actions: '{chosen_actions_func_names}'")
	
		for action_func_name in chosen_actions_func_names:
			chosen_func = getattr(handler_settings.actions_handler.actions, action_func_name)
			kwargs = await chosen_func.kwargs_func(self, chosen_func.parameters_handlers, event)
	
			await self.log_cdp(level="INFO", message=f"Kwargs for '{action_func_name}': '{kwargs}'")
			response_handle_func = chosen_func.response_handle_func
	
			try:
				response = await execute_cdp_command(
						self=self,
						error_mode="raise",
						function=self.devtools_package.get(["fetch", action_func_name]),
						**kwargs
				)
				await self.log_cdp(
						level="AuthRequired",
						message=f"Function '{action_func_name}' response: '{response}'"
				)
	
				if response_handle_func is not None:
					self._nursery_object.start_soon(response_handle_func, self, response)
			except* CDPEndExceptions:
				pass
			except* BaseException as error:
				await self.log_cdp_error(error=error)
	
				if handler_settings.on_error_func is not None:
					handler_settings.on_error_func(self, event, error)
	except* CDPEndExceptions as error:
		raise error
	except* BaseException as error:
		await self.log_cdp_error(error=error)
		raise error


class AuthRequiredSettings(AbstractEventSettings):
	"""
	Settings for handling the 'fetch.AuthRequired' event.

	This dataclass allows configuring the listener for the 'AuthRequired' CDP event,
	including buffer size, the actions to take, and error handling.

	Attributes:
		class_to_use_path (str): The CDP event class path ("fetch.AuthRequired").
		handle_function (handle_auth_required_func_type): The function responsible for processing the event.
		actions_handler (AuthRequiredActionsHandlerSettings): Configuration for the event's actions handler, determining which action to take (e.g., continueWithAuth) and how to build its parameters.
		listen_buffer_size (int): The buffer size for the event listener channel. Defaults to 10.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling. Defaults to None.
	"""
	
	class_to_use_path: str = "fetch.AuthRequired"
	handle_function: handle_auth_required_func_type = _handle_auth_required
	actions_handler: AuthRequiredActionsHandlerSettings
	listen_buffer_size: int = 10
	on_error_func: on_error_func_type = None


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


class ContinueResponseSettings(AbstractActionSettings):
	"""
	Settings for the 'continueResponse' action for a paused request (from RequestPaused event).

	This action is used to modify and continue a request *after* the response has been received but before it is processed by the browser.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments from handlers.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.continueResponse` CDP command. Defaults to None.
		parameters_handlers (Optional[ContinueResponseHandlersSettings]): Configuration for the response parameter handlers that provide modified response details. Defaults to None.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type = _build_kwargs_from_handlers_func
	response_handle_func: response_handle_func_type = None
	parameters_handlers: Optional[ContinueResponseHandlersSettings] = None


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


class FulfillRequestSettings(AbstractActionSettings):
	"""
	Settings for the 'fulfillRequest' action for a paused request (from RequestPaused event).

	This action is used to provide a completely mock response for a request, preventing the browser from sending it to the network.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments from handlers.
		parameters_handlers (FulfillRequestHandlersSettings): Configuration for the mock response parameter handlers.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.fulfillRequest` CDP command. Defaults to None.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type = _build_kwargs_from_handlers_func
	parameters_handlers: FulfillRequestHandlersSettings
	response_handle_func: response_handle_func_type = None


class FailRequestHandlersSettings(AbstractActionParametersHandlersSettings):
	"""
	Configuration for handlers that specify the reason for failing a request using `fetch.failRequest`.

	These handlers provide parameter values for the `fetch.failRequest` CDP command.

	Attributes:
		error_reason (ParameterHandler): Required handler for providing the network error reason (a string from Network.ErrorReason enum, e.g., "Aborted", "AccessDenied").
	"""
	
	error_reason: ParameterHandler


class FailRequestSettings(AbstractActionSettings):
	"""
	Settings for the 'failRequest' action for a paused request (from RequestPaused event).

	This action is used to cause the request to fail with a specific network error reason.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments from handlers.
		parameters_handlers (FailRequestHandlersSettings): Configuration for the error reason handler.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.failRequest` CDP command. Defaults to None.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type = _build_kwargs_from_handlers_func
	parameters_handlers: FailRequestHandlersSettings
	response_handle_func: response_handle_func_type = None


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


class ContinueRequestSettings(AbstractActionSettings):
	"""
	Settings for the 'continueRequest' action for a paused request (from RequestPaused event).

	This action is used to allow the request to proceed, optionally after modifying it.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments from handlers.
		response_handle_func (response_handle_func_type): An optional awaitable function to process the response from the `fetch.continueRequest` CDP command. Defaults to None.
		parameters_handlers (Optional[ContinueRequestHandlersSettings]): Configuration for the request parameter handlers that provide modified request details. Defaults to None.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type = _build_kwargs_from_handlers_func
	response_handle_func: response_handle_func_type = None
	parameters_handlers: Optional[ContinueRequestHandlersSettings] = None


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


class RequestPausedActionsHandlerSettings(AbstractEventActionsHandlerSettings):
	"""
	Settings for handling the 'fetch.RequestPaused' event by choosing and executing specific actions.

	Attributes:
		choose_action_func (request_paused_choose_action_func_type): A function that takes the DevTools instance and the event object and returns a List of action names (Literals) to execute. Defaults to `request_paused_choose_func`.
		actions (Optional[RequestPausedActionsSettings]): Container for the configuration of the available actions. Defaults to None.
	"""
	
	choose_action_func: request_paused_choose_action_func_type = request_paused_choose_func
	actions: Optional[RequestPausedActionsSettings] = None


async def _handle_request_paused(
		self: DevToolsTarget,
		handler_settings: "RequestPausedSettings",
		event: Any
):
	"""
	Handles the 'fetch.RequestPaused' CDP event.

	This function determines which actions to take based on the `choose_action_func`
	defined in the handler settings, builds the necessary keyword arguments for the
	chosen actions using their respective parameter handlers, executes the CDP commands,
	and processes their responses.

	Args:
		self (DevToolsTarget): The DevToolsTarget instance.
		handler_settings (RequestPausedSettings): The configuration settings for handling the 'RequestPaused' event.
		event (Any): The 'RequestPaused' event object received from the CDP.

	Raises:
		BaseException: If a critical error occurs during the event handling process.
	"""
	
	await self.log_cdp(level="INFO", message=f"Started to handle for '{event}'")
	
	try:
		chosen_actions_func_names = handler_settings.actions_handler.choose_action_func(self, event)
		await self.log_cdp(level="INFO", message=f"Chosen actions: '{chosen_actions_func_names}'")
	
		for action_func_name in chosen_actions_func_names:
			chosen_action_func = getattr(handler_settings.actions_handler.actions, action_func_name)
	
			kwargs = await chosen_action_func.kwargs_func(self, chosen_action_func.parameters_handlers, event)
			await self.log_cdp(level="INFO", message=f"Kwargs for '{action_func_name}': '{kwargs}'")
	
			response_handle_func = chosen_action_func.response_handle_func
	
			try:
				response = await execute_cdp_command(
						self=self,
						error_mode="log",
						function=self.devtools_package.get(["fetch", action_func_name]),
						**kwargs
				)
	
				if isinstance(response, ExceptionThrown):
					raise response.exception
	
				await self.log_cdp(
						level="RequestPaused",
						message=f"Function '{action_func_name}' response: '{response}'"
				)
	
				if response_handle_func is not None:
					self._nursery_object.start_soon(response_handle_func, self, response)
			except* CDPEndExceptions:
				pass
			except* BaseException as error:
				await self.log_cdp_error(error=error)
	
				if handler_settings.on_error_func is not None:
					handler_settings.on_error_func(self, event, error)
	except* CDPEndExceptions as error:
		raise error
	except* BaseException as error:
		await self.log_cdp_error(error=error)
		raise error


class RequestPausedSettings(AbstractEventSettings):
	"""
	Settings for handling the 'fetch.RequestPaused' event.

	This dataclass allows configuring the listener for the 'RequestPaused' CDP event,
	including buffer size, the actions to take, and error handling.

	Attributes:
		handle_function (handle_request_paused_func_type): The function responsible for processing the event.
		class_to_use_path (str): The CDP event class path ("fetch.RequestPaused").
		listen_buffer_size (int): The buffer size for the event listener channel. Defaults to 100.
		actions_handler (Optional[RequestPausedActionsHandlerSettings]): Configuration for the event's actions handler, determining which action(s) to take (e.g., continueRequest, fulfillRequest) and how to build their parameters. Defaults to None.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling. Defaults to None.
	"""
	
	handle_function: handle_request_paused_func_type = _handle_request_paused
	class_to_use_path: str = "fetch.RequestPaused"
	listen_buffer_size: int = 100
	actions_handler: Optional[RequestPausedActionsHandlerSettings] = None
	on_error_func: on_error_func_type = None


class FetchHandlersSettings(AbstractDomainHandlersSettings):
	"""
	Container for all handler settings within the Fetch domain.

	Attributes:
		request_paused (Optional[RequestPausedSettings]): Settings for the 'RequestPaused' event handler. Defaults to None.
		auth_required (Optional[AuthRequiredSettings]): Settings for the 'AuthRequired' event handler. Defaults to None.
	"""
	
	request_paused: Optional[RequestPausedSettings] = None
	auth_required: Optional[AuthRequiredSettings] = None


class FetchEnableKwargsSettings(AbstractDomainEnableKwargsSettings):
	"""
	Keyword arguments for enabling the Fetch domain using `fetch.enable`.

	These settings are passed to the `fetch.enable` CDP command when the Fetch domain is activated.

	Attributes:
		patterns (Optional[Sequence[Any]]): A List of request patterns to intercept. Each pattern is typically a dictionary matching the CDP `Fetch.RequestPattern` type. If None, all requests are intercepted. Defaults to None.
		handle_auth_requests (Optional[bool]): Whether to intercept authentication requests (`fetch.AuthRequired` events). If True, `auth_required` events will be emitted. Defaults to None.
	"""
	
	patterns: Optional[Sequence[Any]] = None
	handle_auth_requests: Optional[bool] = None


class FetchSettings(AbstractDomainSettings):
	"""
	Top-level configuration for the Fetch domain.

	This dataclass allows configuring the entire Fetch CDP domain within the DevTools manager,
	including its enabling parameters and event handlers.

	Attributes:
		name (str): The name of the domain ("fetch").
		disable_func_path (str): Path to disable command ("fetch.disable").
		enable_func_path (str): Path to enable command ("fetch.enable").
		exclude_target_types (Sequence[str]): List of target types to exclude.
		include_target_types (Sequence[str]): List of target types to include.
		enable_func_kwargs (Optional[FetchEnableKwargsSettings]): Keyword arguments for enabling the Fetch domain using `fetch.enable`. Defaults to None.
		handlers (FetchHandlersSettings): Container for all handler settings within the Fetch domain (e.g., RequestPaused, AuthRequired). Defaults to None.
	"""
	
	name: str = "fetch"
	disable_func_path: str = "fetch.disable"
	enable_func_path: str = "fetch.enable"
	exclude_target_types: Sequence[str] = Field(default_factory=list)
	include_target_types: Sequence[str] = Field(default_factory=list)
	enable_func_kwargs: Optional[FetchEnableKwargsSettings] = None
	handlers: Optional[FetchHandlersSettings] = None


ContinueWithAuthParameterHandlersSettings.model_rebuild()
ContinueWithAuthParameterHandlersSettings.model_rebuild()
ContinueWithAuthSettings.model_rebuild()
AuthRequiredActionsSettings.model_rebuild()
AuthRequiredActionsHandlerSettings.model_rebuild()
AuthRequiredSettings.model_rebuild()
ContinueResponseHandlersSettings.model_rebuild()
ContinueResponseSettings.model_rebuild()
FulfillRequestHandlersSettings.model_rebuild()
FulfillRequestSettings.model_rebuild()
FailRequestHandlersSettings.model_rebuild()
FailRequestSettings.model_rebuild()
ContinueRequestHandlersSettings.model_rebuild()
ContinueRequestSettings.model_rebuild()
RequestPausedActionsSettings.model_rebuild()
RequestPausedActionsHandlerSettings.model_rebuild()
RequestPausedSettings.model_rebuild()
FetchHandlersSettings.model_rebuild()
FetchEnableKwargsSettings.model_rebuild()
FetchSettings.model_rebuild()
