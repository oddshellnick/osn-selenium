import trio
from typing import (
	Any,
	Awaitable,
	Callable,
	Mapping,
	Optional,
	Sequence,
	TYPE_CHECKING,
	TypedDict
)


if TYPE_CHECKING:
	from osn_selenium.dev_tools.manager import DevToolsTarget


class ParameterHandler(TypedDict):
	"""
	A dictionary defining a parameter handler function and its instances.

	This structure is used within action configurations to specify a function
	that will generate or modify a specific parameter for a CDP command.

	Attributes:
		func (parameter_handler_type): The handler function to be executed. This function should modify a `kwargs` dictionary used for a CDP command.
		instances (Any): The data or configuration specific to this handler instance, passed as the `instances` argument to the `func`.
	"""
	
	func: "parameter_handler_type"
	instances: Any


class AbstractEventActionsSettings:
	"""
	Abstract base class for settings related to actions triggered by a specific event.

	Subclasses should define attributes corresponding to the possible actions
	for the event and implement the `to_dict` method.
	"""
	
	def to_dict(self) -> "AbstractEventActions":
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractEventActions: A dictionary mapping action names to their configurations.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractEventActionsHandler(TypedDict):
	"""
	Abstract TypedDict for the configuration of an event's actions handler.

	This structure defines how to choose and configure the actions to take
	when a specific DevTools event occurs.

	Attributes:
		choose_action_func (event_choose_action_func_type): A function that determines which actions (by name) should be executed for a given event.
		actions (AnyMapping): A dictionary mapping action names (strings) to their full configurations (AbstractAction).
	"""
	
	choose_action_func: "event_choose_action_func_type"
	actions: "AnyMapping"


class AbstractEventActionsHandlerSettings:
	"""
	Abstract base class for settings related to an event's actions handler.

	Subclasses should define attributes for the `choose_action_func` and
	`actions` settings and implement the `to_dict` method.

	Attributes:
		choose_action_func (event_choose_action_func_type): A function that determines which actions (by name) should be executed for a given event.
		actions (AbstractEventActionsSettings): Settings for the available actions.
	"""
	
	choose_action_func: "event_choose_action_func_type"
	actions: AbstractEventActionsSettings
	
	def to_dict(self) -> AbstractEventActionsHandler:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractEventActionsHandler: A dictionary representation of the actions handler settings.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractEvent(TypedDict):
	"""
	Abstract TypedDict representing the configuration for a CDP event listener.

	This structure defines the common components needed to listen for and handle
	a specific Chrome DevTools Protocol (CDP) event.

	Attributes:
		class_to_use_path (str): The dot-separated path to the CDP event class (e.g., "fetch.RequestPaused").
		listen_buffer_size (int): The buffer size for the event listener channel.
		handle_function (AnyCallable): The asynchronous function to execute when an event is received.
		actions_handler (AnyMapping): A dictionary of callback functions and settings specific to the event handler.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling.
	"""
	
	class_to_use_path: str
	listen_buffer_size: int
	handle_function: "AnyCallable"
	actions_handler: "AnyMapping"
	on_error_func: "on_error_func_type"


class AbstractEventSettings:
	"""
	Abstract base class for settings related to a specific DevTools event listener.

	Subclasses should define attributes for buffer size, actions handler,
	and error function, and implement the abstract properties and `to_dict` method.

	Attributes:
		listen_buffer_size (int): The buffer size for the event listener channel.
		actions_handler (AbstractEventActionsHandlerSettings): Configuration for the event's actions handler.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling.
	"""
	
	listen_buffer_size: int
	actions_handler: AbstractEventActionsHandlerSettings
	on_error_func: "on_error_func_type"
	
	@property
	def class_to_use_path(self) -> str:
		"""
		Returns the dot-separated path to the corresponding CDP event class.

		Returns:
			str: The path string.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")
	
	@property
	def handle_function(self) -> "handle_function":
		"""
		Returns the main asynchronous handler function for this event.

		Returns:
			handle_function: The handler function.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")
	
	def to_dict(self) -> AbstractEvent:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractEvent: A dictionary representation of the event settings.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractDomainHandlersSettings:
	"""
	Abstract base class for container of all handler settings within a DevTools domain.

	Subclasses should define attributes for each event handler within the domain
	and implement the `to_dict` method.
	"""
	
	def to_dict(self) -> "AbstractDomainHandlers":
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractDomainHandlers: A dictionary mapping event names to their handler configurations.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractDomainEnableKwargsSettings:
	"""
	Abstract base class for keyword arguments used to enable a DevTools domain.

	Subclasses should define attributes corresponding to the parameters
	of the domain's enable function and implement the `to_dict` method.
	"""
	
	def to_dict(self) -> "AbstractDomainEnableKwargs":
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractDomainEnableKwargs: A dictionary of keyword arguments for the enable function.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractDomain(TypedDict):
	"""
	Abstract TypedDict for the complete configuration of a DevTools domain.

	This structure is used internally by the DevTools manager to configure a
	specific domain, including how to enable/disable it and what event handlers to use.

	Attributes:
		name (str): The name of the domain (e.g., 'fetch').
		enable_func_path (str): The dot-separated path to the function to enable the domain (e.g., "fetch.enable").
		enable_func_kwargs (Optional[AnyMapping]): Keyword arguments for the enable function.
		disable_func_path (str): The dot-separated path to the function to disable the domain (e.g., "fetch.disable").
		handlers (AnyMapping): A dictionary mapping event names to their configured handlers (AbstractEvent).
	"""
	
	name: str
	enable_func_path: str
	enable_func_kwargs: Optional["AnyMapping"]
	disable_func_path: str
	handlers: "AnyMapping"


class AbstractDomainSettings:
	"""
	Abstract base class for the top-level configuration of a DevTools domain.

	Subclasses should define attributes for enable keyword arguments and handlers,
	and implement the abstract properties and `to_dict` method.

	Attributes:
		enable_func_kwargs (Optional[AbstractDomainEnableKwargsSettings]): Keyword arguments for enabling the domain.
		handlers (AbstractDomainHandlersSettings): Container for all handler settings within the domain.
	"""
	
	enable_func_kwargs: Optional[AbstractDomainEnableKwargsSettings]
	handlers: AbstractDomainHandlersSettings
	
	@property
	def disable_func_path(self) -> str:
		"""
		Returns the dot-separated path to the function used to disable the domain.

		Returns:
			str: The path string.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")
	
	@property
	def enable_func_path(self) -> str:
		"""
		Returns the dot-separated path to the function used to enable the domain.

		Returns:
			str: The path string.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")
	
	@property
	def name(self) -> str:
		"""
		Returns the name of the DevTools domain.

		Returns:
			str: The domain name.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")
	
	def to_dict(self) -> AbstractDomain:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractDomain: A dictionary representation of the domain settings.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractActionParametersHandlersSettings:
	"""
	Abstract base class for settings related to parameter handlers for a specific action.

	Subclasses should define attributes corresponding to the parameters
	of the action's CDP command and implement the `to_dict` method.
	"""
	
	def to_dict(self) -> "AbstractActionParametersHandlers":
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractActionParametersHandlers: A dictionary mapping parameter names to their handler configurations.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


class AbstractAction(TypedDict):
	"""
	Abstract TypedDict for the configuration of a specific action triggered by an event.

	This structure defines how to build the arguments for a CDP command
	and how to handle its response.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the CDP command.
		response_handle_func (response_handle_func_type): An optional function to process the response from the CDP command.
		parameters_handlers (AnyMapping): A dictionary mapping parameter names to their handler configurations (ParameterHandler).
	"""
	
	kwargs_func: "build_kwargs_from_handlers_func_type"
	response_handle_func: "response_handle_func_type"
	parameters_handlers: "AnyMapping"


class AbstractActionSettings:
	"""
	Abstract base class for settings related to a specific action triggered by an event.

	Subclasses should define attributes for response handling and parameter handlers,
	and implement the abstract property and `to_dict` method.

	Attributes:
		response_handle_func (response_handle_func_type): An optional function to process the response from the CDP command.
		parameters_handlers (AbstractActionParametersHandlersSettings): Settings for the action's parameter handlers.
	"""
	
	response_handle_func: "response_handle_func_type"
	parameters_handlers: AbstractActionParametersHandlersSettings
	
	@property
	def kwargs_func(self) -> "build_kwargs_from_handlers_func_type":
		"""
		Returns the function used to build keyword arguments for the action's CDP command.

		Returns:
			build_kwargs_from_handlers_func_type: The kwargs building function.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")
	
	def to_dict(self) -> AbstractAction:
		"""
		Converts the settings object to its dictionary representation.

		Returns:
			AbstractAction: A dictionary representation of the action settings.
		"""
		
		raise NotImplementedError("This method must be implemented in a subclass.")


kwargs_type = dict[str, Any]
kwargs_output_type = Awaitable[kwargs_type]
build_kwargs_from_handlers_func_type = Optional[
	Callable[
		["DevToolsTarget", Mapping[str, Optional[ParameterHandler]], Any],
		kwargs_output_type
	]
]
parameter_handler_type = Callable[["DevToolsTarget", trio.Event, Any, Any, dict[str, Any]], Awaitable[None]]
event_choose_action_func_type = Callable[["DevToolsTarget", Any], Sequence[str]]
handle_function = Callable[["DevToolsTarget", Any, Any], Awaitable[None]]
response_handle_func_type = Optional[Callable[["DevToolsTarget", Any], Awaitable[Any]]]
on_error_func_type = Optional[Callable[["DevToolsTarget", Any, BaseException], None]]
AnyMapping = Mapping[str, Any]
AnyCallable = Callable[..., Any]
AbstractDomainHandlers = Mapping[str, AbstractEvent]
AbstractDomainEnableKwargs = Mapping[str, Any]
AbstractEventActions = Mapping[str, AbstractAction]
AbstractActionParametersHandlers = Mapping[str, ParameterHandler]
