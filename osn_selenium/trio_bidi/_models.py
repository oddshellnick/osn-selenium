import trio
import threading
from dataclasses import dataclass, field
from typing import (
	Any,
	Dict,
	Optional,
	Self
)
from osn_selenium.trio_bidi._typehints import (
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["BiDiTask", "BiDiTaskContainer", "W3CTask", "W3CTaskContainer"]


@dataclass(slots=True)
class W3CTask:
	"""
	Representation of a W3C WebDriver task.

	Attributes:
		command (str): The command name.
		request_params (REQUEST_PARAMS_TYPEHINT): The command parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.
	"""
	
	command: str
	params: REQUEST_PARAMS_TYPEHINT
	context_id: Optional[str]
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> Self:
		"""
		Creates a W3CTask instance from a dictionary.

		Args:
			data (Dict[str, Any]): The dictionary containing task data.

		Returns:
			Self: A new W3CTask instance.
		"""
		
		return cls(
				command=data["command"],
				params=data["params"],
				context_id=data["context_id"],
		)
	
	def to_dict(self) -> Dict[str, Any]:
		"""
		Converts the task to a dictionary.

		Returns:
			Dict[str, Any]: The task as a dictionary.
		"""
		
		return {
			"command": self.command,
			"params": self.params,
			"context_id": self.context_id,
		}


@dataclass(slots=True)
class W3CTaskContainer:
	"""
	Container for a W3C task including response and synchronization event.

	Attributes:
		task (W3CTask): The W3C task.
		response (Dict[str, Any]): The response and error information.
		pending_event (threading.Event): Event to wait for task completion.
	"""
	
	task: W3CTask
	response: Dict[str, Any] = field(default_factory=lambda: {"response": None, "error": None})
	pending_event: threading.Event = field(default_factory=threading.Event)
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> Self:
		"""
		Creates a W3CTaskContainer instance from a dictionary.

		Args:
			data (Dict[str, Any]): The dictionary containing container data.

		Returns:
			Self: A new W3CTaskContainer instance.
		"""
		
		return cls(
				task=W3CTask.from_dict(data["task"]),
				response=data["response"],
				pending_event=data["pending_event"],
		)
	
	def to_dict(self) -> Dict[str, Any]:
		"""
		Converts the container to a dictionary.

		Returns:
			Dict[str, Any]: The container as a dictionary.
		"""
		
		return {
			"task": self.task.to_dict(),
			"response": self.response,
			"pending_event": self.pending_event,
		}


@dataclass(slots=True)
class BiDiTask:
	"""
	Representation of a WebDriver BiDi task.

	Attributes:
		id (int): The task ID.
		method (str): The BiDi method.
		request_params (REQUEST_PARAMS_TYPEHINT): The BiDi parameters.
	"""
	
	id: int
	method: str
	params: REQUEST_PARAMS_TYPEHINT
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> Self:
		"""
		Creates a BiDiTask instance from a dictionary.

		Args:
			data (Dict[str, Any]): The dictionary containing task data.

		Returns:
			Self: A new BiDiTask instance.
		"""
		
		return cls(id=data["id"], method=data["method"], params=data["params"])
	
	def to_dict(self) -> Dict[str, Any]:
		"""
		Converts the task to a dictionary.

		Returns:
			Dict[str, Any]: The task as a dictionary.
		"""
		
		return {"id": self.id, "method": self.method, "params": self.params}


@dataclass(slots=True)
class BiDiTaskContainer:
	"""
	Container for a BiDi task including response and synchronization event.

	Attributes:
		task (BiDiTask): The BiDi task.
		response (Dict[str, Any]): The response data.
		pending_event (trio.Event): Trio event to wait for task completion.
	"""
	
	task: BiDiTask
	response: Dict[str, Any] = field(default_factory=dict)
	pending_event: trio.Event = field(default_factory=trio.Event)
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> Self:
		"""
		Creates a BiDiTaskContainer instance from a dictionary.

		Args:
			data (Dict[str, Any]): The dictionary containing container data.

		Returns:
			Self: A new BiDiTaskContainer instance.
		"""
		
		return cls(
				task=BiDiTask.from_dict(data["task"]),
				response=data["response"],
				pending_event=data["pending_event"],
		)
	
	def to_dict(self) -> Dict[str, Any]:
		"""
		Converts the container to a dictionary.

		Returns:
			Dict[str, Any]: The container as a dictionary.
		"""
		
		return {
			"task": self.task.to_dict(),
			"response": self.response,
			"pending_event": self.pending_event,
		}
