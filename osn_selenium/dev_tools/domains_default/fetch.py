import trio
from datetime import datetime
from osn_selenium._base_models import DictModel
from osn_selenium.dev_tools._exception_helpers import log_exception
from typing import (
	Any,
	Dict,
	List,
	Literal,
	TYPE_CHECKING,
	Union
)


__all__ = [
	"HeaderInstance",
	"auth_required_choose_func",
	"headers_handler",
	"on_error_func",
	"request_paused_choose_func"
]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target import DevToolsTarget
	from osn_selenium.dev_tools.domains.fetch import request_paused_actions_literal, auth_required_actions_literal


def request_paused_choose_func(self: "DevToolsTarget", event: Any) -> List["request_paused_actions_literal"]:
	"""
	Default function to choose actions for a 'fetch.RequestPaused' event.

	This default implementation always chooses to 'continue_request'.
	Users can provide their own function to implement custom logic for
	deciding which actions to take based on the event details.

	Args:
		self ("DevToolsTarget"): The DevToolsTarget instance.
		event (Any): The 'RequestPaused' event object.

	Returns:
		List[request_paused_actions_literal]: A list of action names to be executed.
	"""
	
	return ["continue_request"]


def on_error_func(self: "DevToolsTarget", event: Any, error: BaseException):
	"""
	Default error handling function for DevTools event listeners.

	This function simply logs the error using the internal error logging utility.
	Users can provide their own function to implement custom error handling logic.

	Args:
		self ("DevToolsTarget"): The DevToolsTarget instance.
		event (Any): The event object that was being processed when the error occurred.
		error (BaseException): The exception that was raised.
	"""
	
	log_exception(
			exception=error,
			extra_data={
				"datetime": datetime.now(),
				"target object data": self.target_data.model_dump(),
				"event": event
			}
	)


class HeaderInstance(DictModel):
	"""
	Type definition for header modification instructions used by the `headers_handler`.

	This TypedDict is used to specify how a header should be modified when intercepting network requests using DevTools.
	It includes the new value for the header and an instruction on how to apply the change (set, set if exists, remove).

	Attributes:
		value (Union[str, Any]): The new value to set for the header. Can be a string or any other type that can be converted to a string for the header value.
		instruction (Literal["set", "set_exist", "remove"]): Specifies the type of modification to apply to the header.

			- "set": Sets the header to the provided `value`, overwriting any existing value or adding it if not present.
			- "set_exist": Sets the header to the provided `value` only if the header already exists in the request.
			- "remove": Removes the header from the request if it exists.
	"""
	
	value: Union[str, Any]
	instruction: Union[Literal["set", "set_exist", "remove"], Any]


async def headers_handler(
		self: "DevToolsTarget",
		ready_event: trio.Event,
		headers_instances: Dict[str, HeaderInstance],
		event: Any,
		kwargs: Dict[str, Any]
):
	"""
	A parameter handler function to modify request headers.

	This handler processes a dictionary of header modification instructions (`headers_instances`)
	and applies them to the request headers found in the `event` object. The modified headers
	are then added to the `kwargs` dictionary, which will be used for a CDP command
	like `fetch.continueRequest`.

	Args:
		self ("DevToolsTarget"): The DevToolsTarget instance.
		ready_event (trio.Event): A Trio event to signal when the handler has completed its work.
		headers_instances (Dict[str, HeaderInstance]): A dictionary where keys are header names
			and values are `HeaderInstance` objects defining the modification.
		event (Any): The CDP event object (e.g., `RequestPaused`) containing the original request headers.
		kwargs (Dict[str, Any]): The dictionary of keyword arguments to which the modified headers will be added.

	Raises:
		Exception: If an error occurs during header modification.
	"""
	
	try:
		header_entry_class = self.devtools_package.get("fetch.HeaderEntry")
		headers = {name: value for name, value in event.request.headers.items()}
	
		for name, instance in headers_instances.items():
			value = instance.value
			instruction = instance.instruction
	
			if instruction == "set":
				headers[name] = value
				continue
	
			if instruction == "set_exist":
				if name in headers:
					headers[name] = value
	
				continue
	
			if instruction == "remove":
				headers.pop(name, None)
	
				continue
	
		kwargs["headers"] = [
			header_entry_class(name=name, value=value)
			for name, value in headers.items()
		]
	
		ready_event.set()
	except BaseException as error:
		await self.log_cdp_error(error=error)
		raise error


def auth_required_choose_func(self: "DevToolsTarget", event: Any) -> List["auth_required_actions_literal"]:
	"""
	Default function to choose actions for a 'fetch.AuthRequired' event.

	This default implementation always chooses to 'continue_with_auth'.
	Users can provide their own function to implement custom logic for
	deciding which actions to take based on the event details.

	Args:
		self ("DevToolsTarget"): The DevToolsTarget instance.
		event (Any): The 'AuthRequired' event object.

	Returns:
		List[auth_required_actions_literal]: A list of action names to be executed.
	"""
	
	return ["continue_with_auth"]
