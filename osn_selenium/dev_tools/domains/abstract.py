import trio
from osn_selenium._base_models import DictModel
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Mapping,
	Optional,
	Sequence,
	TYPE_CHECKING
)


__all__ = [
	"AbstractActionParametersHandlers",
	"AbstractActionParametersHandlersSettings",
	"AbstractActionSettings",
	"AbstractDomainEnableKwargs",
	"AbstractDomainEnableKwargsSettings",
	"AbstractDomainHandlers",
	"AbstractDomainHandlersSettings",
	"AbstractDomainSettings",
	"AbstractEventActions",
	"AbstractEventActionsHandlerSettings",
	"AbstractEventActionsSettings",
	"AbstractEventSettings",
	"AnyCallable",
	"AnyMapping",
	"ParameterHandler",
	"build_kwargs_from_handlers_func_type",
	"event_choose_action_func_type",
	"handle_function",
	"kwargs_output_type",
	"kwargs_type",
	"on_error_func_type",
	"parameter_handler_type",
	"response_handle_func_type"
]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target.base import BaseMixin as BaseTargetMixin
else:
	BaseTargetMixin = Any

kwargs_type = Dict[str, Any]
kwargs_output_type = Coroutine[Any, Any, kwargs_type]

build_kwargs_from_handlers_func_type = Optional[
	Callable[
		[BaseTargetMixin, Mapping[str, Optional["ParameterHandler"]], Any],
		kwargs_output_type
	]
]
parameter_handler_type = Callable[
	[BaseTargetMixin, trio.Event, Any, Any, Dict[str, Any]],
	Coroutine[Any, Any, None]
]
event_choose_action_func_type = Callable[[BaseTargetMixin, Any], Sequence[str]]
handle_function = Callable[[BaseTargetMixin, Any, Any], Coroutine[Any, Any, None]]
response_handle_func_type = Optional[Callable[[BaseTargetMixin, Any], Coroutine[Any, Any, Any]]]
on_error_func_type = Optional[Callable[[BaseTargetMixin, Any, BaseException], None]]
AnyMapping = Mapping[str, Any]
AnyCallable = Callable[..., Any]


class ParameterHandler(DictModel):
	"""
	A dictionary defining a parameter handler function and its instances.

	This structure is used within action configurations to specify a function
	that will generate or modify a specific parameter for a CDP command.

	Attributes:
		func (parameter_handler_type): The handler function to be executed. This function should modify a `kwargs` dictionary used for a CDP command.
		instances (Any): The data or configuration specific to this handler instance, passed as the `instances` argument to the `func`.
	"""
	
	func: parameter_handler_type
	instances: Any


class AbstractEventActionsSettings(DictModel):
	"""
	Abstract base class for settings related to actions triggered by a specific event.

	Subclasses should define attributes corresponding to the possible actions
	for the event and implement the `to_dict` method.
	"""
	
	pass


class AbstractEventActionsHandlerSettings(DictModel):
	"""
	Abstract base class for settings related to an event's actions handler.

	Subclasses should define attributes for the `choose_action_func` and
	`actions` settings and implement the `to_dict` method.

	Attributes:
		choose_action_func (event_choose_action_func_type): A function that determines which actions (by name) should be executed for a given event.
		actions (AbstractEventActionsSettings): Settings for the available actions.
	"""
	
	choose_action_func: event_choose_action_func_type
	actions: AbstractEventActionsSettings


class AbstractEventSettings(DictModel):
	"""
	Abstract base class for settings related to a specific DevTools event listener.

	Subclasses should define attributes for buffer size, actions handler,
	and error function, and implement the abstract properties and `to_dict` method.

	Attributes:
		handle_function (handle_function): The function responsible for processing the event.
		class_to_use_path (str): The dot-separated path to the CDP event class (e.g., "fetch.RequestPaused").
		listen_buffer_size (int): The buffer size for the event listener channel.
		actions_handler (AbstractEventActionsHandlerSettings): Configuration for the event's actions handler.
		on_error_func (on_error_func_type): An optional function to call if an error occurs during event handling.
	"""
	
	handle_function: handle_function
	class_to_use_path: str
	listen_buffer_size: int
	actions_handler: AbstractEventActionsHandlerSettings
	on_error_func: on_error_func_type


class AbstractDomainHandlersSettings(DictModel):
	"""
	Abstract base class for container of all handler settings within a DevTools domain.

	Subclasses should define attributes for each event handler within the domain
	and implement the `to_dict` method.
	"""
	
	pass


class AbstractDomainEnableKwargsSettings(DictModel):
	"""
	Abstract base class for keyword arguments used to enable a DevTools domain.

	Subclasses should define attributes corresponding to the parameters
	of the domain's enable function and implement the `to_dict` method.
	"""
	
	pass


class AbstractDomainSettings(DictModel):
	"""
	Abstract base class for the top-level configuration of a DevTools domain.

	Subclasses should define attributes for enable keyword arguments and handlers,
	and implement the abstract properties and `to_dict` method.

	Attributes:
		name (str): The name of the domain (e.g., "fetch").
		disable_func_path (str): The path to the CDP command used to disable the domain.
		enable_func_path (str): The path to the CDP command used to enable the domain.
		exclude_target_types (Sequence[str]): List of target types to exclude from this domain's activation.
		include_target_types (Sequence[str]): List of target types to specifically include for this domain's activation.
		enable_func_kwargs (Optional[AbstractDomainEnableKwargsSettings]): Keyword arguments for enabling the domain.
		handlers (AbstractDomainHandlersSettings): Container for all handler settings within the domain.
	"""
	
	name: str
	disable_func_path: str
	enable_func_path: str
	exclude_target_types: Sequence[str]
	include_target_types: Sequence[str]
	enable_func_kwargs: Optional[AbstractDomainEnableKwargsSettings]
	handlers: AbstractDomainHandlersSettings


class AbstractActionParametersHandlersSettings(DictModel):
	"""
	Abstract base class for settings related to parameter handlers for a specific action.

	Subclasses should define attributes corresponding to the parameters
	of the action's CDP command and implement the `to_dict` method.
	"""
	
	pass


class AbstractActionSettings(DictModel):
	"""
	Abstract base class for settings related to a specific action triggered by an event.

	Subclasses should define attributes for response handling and parameter handlers,
	and implement the abstract property and `to_dict` method.

	Attributes:
		kwargs_func (build_kwargs_from_handlers_func_type): Function to build keyword arguments for the action from handlers.
		response_handle_func (response_handle_func_type): An optional function to process the response from the CDP command.
		parameters_handlers (AbstractActionParametersHandlersSettings): Settings for the action's parameter handlers.
	"""
	
	kwargs_func: build_kwargs_from_handlers_func_type
	response_handle_func: response_handle_func_type
	parameters_handlers: AbstractActionParametersHandlersSettings


AbstractDomainHandlers = Mapping[str, AbstractEventSettings]
AbstractDomainEnableKwargs = Mapping[str, Any]
AbstractEventActions = Mapping[str, AbstractActionSettings]
AbstractActionParametersHandlers = Mapping[str, ParameterHandler]

AbstractActionParametersHandlersSettings.model_rebuild()
AbstractActionSettings.model_rebuild()
ParameterHandler.model_rebuild()
AbstractEventActionsSettings.model_rebuild()
AbstractEventActionsHandlerSettings.model_rebuild()
AbstractEventSettings.model_rebuild()
AbstractDomainHandlersSettings.model_rebuild()
AbstractDomainEnableKwargsSettings.model_rebuild()
AbstractDomainSettings.model_rebuild()
