from selenium import webdriver
from osn_selenium.types import (
	DictModel,
	ExtraDictModel
)
from typing import (
	Any,
	Callable,
	List,
	Literal,
	Mapping,
	Union
)


class _MoveStep:
	"""
	Internal helper class representing a step in a movement calculation.

	Attributes:
		amplitude_x (int): The horizontal component or amplitude of this step.
		amplitude_y (int): The vertical component or amplitude of this step.
		index (int): An index identifying this step's position in a sequence.
	"""
	
	def __init__(self, amplitude_x: int, amplitude_y: int, index: int):
		self.amplitude_x: int = amplitude_x
		self.amplitude_y: int = amplitude_y
		self.index: int = index
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return (
				f"MoveStep(amplitude_x={self.amplitude_x}, amplitude_y={self.amplitude_y})"
		)


class TextInputPart:
	"""
	Represents a segment of text input with an associated duration.

	Attributes:
		text (str): The chunk of text for this part.
		duration (int): Duration (milliseconds) associated with this part.
	"""
	
	def __init__(self, text: str, duration: int):
		self.text: str = text
		self.duration: int = duration
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return f"TextInputPart(text={self.text}, duration={self.duration})"


class ScrollDelta:
	"""
	Represents the change in scroll position (dx, dy).

	Attributes:
		x (int): Horizontal scroll amount.
		y (int): Vertical scroll amount.
	"""
	
	def __init__(self, x: int, y: int):
		self.x: int = x
		self.y: int = y
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return f"ScrollDelta(x={self.x}, y={self.y})"


class Point:
	"""
	Represents a 2D point with integer coordinates (x, y).

	Attributes:
		x (int): The horizontal coordinate.
		y (int): The vertical coordinate.
	"""
	
	def __init__(self, x: int, y: int):
		self.x: int = x
		self.y: int = y
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return f"ActionPoint(x={self.x}, y={self.y})"
	
	def __eq__(self, other: "Point") -> bool:
		return self.x == other.x and self.y == other.y
	
	def __ne__(self, other: "Point") -> bool:
		return not self.__eq__(other)


class ScrollPart:
	"""
	Represents a segment of a simulated scroll action.

	Attributes:
		point (Point): Coordinate point before this scroll segment.
		delta (ScrollDelta): Scroll amount (dx, dy) for this segment.
		duration (int): Duration (milliseconds) for this scroll segment.
	"""
	
	def __init__(self, point: Point, delta: ScrollDelta, duration: int):
		self.point: Point = point
		self.delta: ScrollDelta = delta
		self.duration: int = duration
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return (
				f"ScrollPart(point={self.point}, delta={self.delta}, duration={self.duration})"
		)


class MoveOffset:
	"""
	Represents a 2D offset or displacement (dx, dy).

	Attributes:
		x (int): Horizontal offset component.
		y (int): Vertical offset component.
	"""
	
	def __init__(self, x: int, y: int):
		self.x: int = x
		self.y: int = y
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return f"MoveOffset(x={self.x}, y={self.y})"


class MovePart:
	"""
	Represents a segment of a simulated mouse movement.

	Attributes:
		point (Point): Target coordinate point.
		offset (MoveOffset): Offset (dx, dy) for this segment.
		duration (int): Duration (milliseconds) for this movement segment.
	"""
	
	def __init__(self, point: Point, offset: MoveOffset, duration: int):
		self.point: Point = point
		self.offset: MoveOffset = offset
		self.duration: int = duration
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __str__(self) -> str:
		return (
				f"MovePart(point={self.point}, offset={self.offset}, duration={self.duration})"
		)


class FlagDefinition(DictModel):
	"""
	Defines a browser flag with name, command, type, and how it is applied.

	Attributes:
		name (str): Internal name of the flag.
		command (str): Command-line argument or key.
		type (Literal): Category of the flag (e.g., argument, attribute).
		mode (Literal): How the flag is applied (e.g., startup, webdriver).
		adding_validation_function (Callable): Validator function for the value.
	"""
	
	name: str
	command: str
	type: Literal["argument", "experimental_option", "attribute", "blink_feature"]
	mode: Literal["webdriver_option", "startup_argument", "both"]
	adding_validation_function: Callable[[Any], bool]


class FlagType(DictModel):
	"""
	Represents callable interfaces for setting and managing browser flags.

	Attributes:
		set_flag_function (Callable): Function to set a single flag.
		remove_flag_function (Callable): Function to remove a flag.
		set_flags_function (Callable): Function to set multiple flags.
		update_flags_function (Callable): Function to update multiple flags.
		clear_flags_function (Callable): Function to clear all flags.
		build_options_function (Callable): Builds webdriver options.
		build_start_args_function (Callable): Builds command-line arguments.
	"""
	
	set_flag_function: Callable[[FlagDefinition, Any], None]
	remove_flag_function: Callable[[str], None]
	set_flags_function: Callable[[ExtraDictModel], None]
	update_flags_function: Callable[[ExtraDictModel], None]
	clear_flags_function: Callable[..., None]
	build_options_function: Callable[["_any_webdriver_option_type"], "_any_webdriver_option_type"]
	build_start_args_function: Callable[..., List[str]]


class FlagNotDefined:
	"""
	A sentinel class to indicate that a flag definition was not found.
	"""
	
	pass


_any_webdriver_option_type = Union[
	webdriver.ChromeOptions,
	webdriver.EdgeOptions,
	webdriver.FirefoxOptions
]

AutoplayPolicyType = Literal["user-gesture-required", "no-user-gesture-required"]

ValidAutoplayPolicies = ["user-gesture-required", "no-user-gesture-required"]

LogLevelType = Literal[0, 1, 2, 3]
ValidLogLevels = [0, 1, 2, 3]

UseGLType = Literal["desktop", "egl", "swiftshader"]
ValidUseGLs = ["desktop", "egl", "swiftshader"]

_any_flags_mapping = Mapping[str, Any]

_blink_webdriver_option_type = Union[webdriver.ChromeOptions, webdriver.EdgeOptions]
