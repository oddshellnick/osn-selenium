from selenium import webdriver
from typing import (
	Any,
	Callable,
	Literal,
	Mapping,
	TypedDict,
	Union
)


class _MoveStep:
	"""
	Internal helper class representing a step in a movement calculation.

	Likely used within algorithms that generate multi-step paths for simulations.

	Attributes:
		amplitude_x (int): The horizontal component or amplitude of this step.
		amplitude_y (int): The vertical component or amplitude of this step.
		index (int): An index identifying this step's position in a sequence.
	"""
	
	def __init__(self, amplitude_x: int, amplitude_y: int, index: int):
		"""
		Initializes a _MoveStep instance.

		Args:
			amplitude_x (int): The horizontal amplitude.
			amplitude_y (int): The vertical amplitude.
			index (int): The index of the step.
		"""
		
		self.amplitude_x: int = amplitude_x
		self.amplitude_y: int = amplitude_y
		self.index: int = index
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"MoveStep(amplitude_x={self.amplitude_x}, amplitude_y={self.amplitude_y})"


class TextInputPart:
	"""
	Represents a segment of text input with an associated duration.

	Used to break down a larger text input into smaller chunks for simulating
	human-like typing with pauses between parts.

	Attributes:
		text (str): The chunk of text for this part.
		duration (int): The duration (milliseconds)
					   associated with this part, often representing a pause before or after typing it.
	"""
	
	def __init__(self, text: str, duration: int):
		"""
		Initializes a TextInputPart instance.

		Args:
			text (str): The text segment.
			duration (int): The duration associated with this segment.
		"""
		
		self.text: str = text
		self.duration: int = duration
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"TextInputPart(text={self.text}, duration={self.duration})"


class ScrollDelta:
	"""
	Represents the change in scroll position (dx, dy).

	Used to specify the amount to scroll horizontally and vertically.

	Attributes:
		x (int): The horizontal scroll amount. Positive scrolls right, negative left.
		y (int): The vertical scroll amount. Positive scrolls down, negative up.
	"""
	
	def __init__(self, x: int, y: int):
		"""
		Initializes a ScrollDelta instance.

		Args:
			x (int): The horizontal scroll amount.
			y (int): The vertical scroll amount.
		"""
		
		self.x: int = x
		self.y: int = y
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"ScrollDelta(x={self.x}, y={self.y})"


class ActionPoint:
	"""
	Represents a 2D point with integer coordinates (x, y).

	Commonly used to define locations on a screen or canvas. Includes
	equality comparison methods.

	Attributes:
		x (int): The horizontal coordinate.
		y (int): The vertical coordinate.
	"""
	
	def __init__(self, x: int, y: int):
		"""
		Initializes an ActionPoint instance.

		Args:
			x (int): The horizontal coordinate.
			y (int): The vertical coordinate.
		"""
		
		self.x: int = x
		self.y: int = y
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"ActionPoint(x={self.x}, y={self.y})"
	
	def __eq__(self, other: "ActionPoint") -> bool:
		"""
		Checks if this ActionPoint is equal to another ActionPoint.

		Args:
			other (object): The object to compare against.

		Returns:
			bool: True if `other` is an ActionPoint with the same x and y coordinates, False otherwise.
		"""
		
		return self.x == other.x and self.y == other.y
	
	def __ne__(self, other: "ActionPoint") -> bool:
		"""
		Checks if this ActionPoint is not equal to another ActionPoint.

		Args:
			other (object): The object to compare against.

		Returns:
			bool: True if `other` is not an ActionPoint or has different coordinates, False otherwise.
		"""
		
		return not self.__eq__(other)


class ScrollPart:
	"""
	Represents a segment of a simulated scroll action.

	Combines the conceptual current point, the scroll delta for this segment,
	and the duration associated with performing this scroll segment.

	Attributes:
		point (ActionPoint): The conceptual coordinate point before this scroll segment.
		delta (ScrollDelta): The scroll amount (dx, dy) for this segment.
		duration (int): The duration (milliseconds) for this scroll segment.
	"""
	
	def __init__(self, point: ActionPoint, delta: ScrollDelta, duration: int):
		"""
		Initializes a ScrollPart instance.

		Args:
			point (ActionPoint): The conceptual point before scrolling.
			delta (ScrollDelta): The scroll amount for this segment.
			duration (int): The duration of this scroll segment.
		"""
		
		self.point: ActionPoint = point
		self.delta: ScrollDelta = delta
		self.duration: int = duration
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"ScrollPart(point={self.point}, delta={self.delta}, duration={self.duration})"


class MoveOffset:
	"""
	Represents a 2D offset or displacement (dx, dy).

	Used to specify relative movement distances.

	Attributes:
		x (int): The horizontal offset component.
		y (int): The vertical offset component.
	"""
	
	def __init__(self, x: int, y: int):
		"""
		Initializes a MoveOffset instance.

		Args:
			x (int): The horizontal offset.
			y (int): The vertical offset.
		"""
		
		self.x: int = x
		self.y: int = y
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"MoveOffset(x={self.x}, y={self.y})"


class MovePart:
	"""
	Represents a segment of a simulated mouse movement.

	Combines the target point, the offset required to reach it from the previous
	point, and the duration associated with this segment.

	Attributes:
		point (ActionPoint): The target coordinate point for this movement segment.
		offset (MoveOffset): The offset (dx, dy) representing the movement in this segment.
		duration (int): The duration (milliseconds) for this movement segment.
	"""
	
	def __init__(self, point: ActionPoint, offset: MoveOffset, duration: int):
		"""
		Initializes a MovePart instance.

		Args:
			point (ActionPoint): The target point of the segment.
			offset (MoveOffset): The movement offset for the segment.
			duration (int): The duration of the segment.
		"""
		
		self.point: ActionPoint = point
		self.offset: MoveOffset = offset
		self.duration: int = duration
	
	def __repr__(self) -> str:
		"""Returns a string representation suitable for debugging."""
		
		return self.__str__()
	
	def __str__(self) -> str:
		"""Returns a user-friendly string representation."""
		
		return f"MovePart(point={self.point}, offset={self.offset}, duration={self.duration})"


class JS_Scripts(TypedDict):
	"""
	Type definition for a collection of JavaScript script snippets.

	This TypedDict defines the structure for storing a collection of JavaScript snippets as strings.
	It is used to organize and access various JavaScript functionalities intended to be executed
	within a browser context, typically via Selenium WebDriver's `execute_script` method.

	Attributes:
		check_element_in_viewport (str): JavaScript code to check if an element is fully within the current browser viewport. Expects the element as arguments[0].
		get_document_scroll_size (str): JavaScript code to retrieve the total scrollable width and height of the document.
		get_element_css (str): JavaScript code to retrieve all computed CSS style properties of a DOM element. Expects the element as arguments[0].
		get_element_rect_in_viewport (str): JavaScript code to get the bounding rectangle (position and dimensions) of an element relative to the viewport. Expects the element as arguments[0].
		get_random_element_point_in_viewport (str): JavaScript code to calculate a random point (x, y coordinates) within the visible portion of a given element in the viewport. Expects the element as arguments[0].
		get_viewport_position (str): JavaScript code to get the current scroll position (X and Y offsets) of the viewport.
		get_viewport_rect (str): JavaScript code to get the viewport's position (scroll offsets) and dimensions (width, height).
		get_viewport_size (str): JavaScript code to get the current dimensions (width and height) of the viewport.
		stop_window_loading (str): JavaScript code to stop the current window's page loading process (`window.stop()`).
		open_new_tab (str): JavaScript code to open a new browser tab/window using `window.open()`. Expects an optional URL as arguments[0].
	"""
	
	check_element_in_viewport: str
	get_document_scroll_size: str
	get_element_css: str
	get_element_rect_in_viewport: str
	get_random_element_point_in_viewport: str
	get_viewport_position: str
	get_viewport_rect: str
	get_viewport_size: str
	stop_window_loading: str
	open_new_tab: str


class FlagDefinition(TypedDict):
	"""
	Defines the structure for a single browser flag or option.

	Attributes:
		name (str): The internal name of the flag (e.g., "headless_mode").
		command (str): The command-line argument string or option key used by WebDriver
			(e.g., "--headless", "debuggerAddress").
		type (Literal["argument", "experimental_option", "attribute", "blink_feature"]):
			The category of the flag (e.g., command-line argument, experimental option).
		mode (Literal["webdriver_option", "startup_argument", "both"]):
			Indicates how the flag is applied:
			- "webdriver_option": Applied via Selenium's Options object.
			- "startup_argument": Applied as a command-line argument when launching the browser process.
			- "both": Applied in both ways.
		adding_validation_function (Callable[[Any], bool]): A callable that validates the value
			before the flag is added. Returns True if valid, False otherwise.
	"""
	
	name: str
	command: str
	type: Literal["argument", "experimental_option", "attribute", "blink_feature"]
	mode: Literal["webdriver_option", "startup_argument", "both"]
	adding_validation_function: Callable[[Any], bool]


class FlagType(TypedDict):
	"""
	Defines the callable interfaces for managing different types of browser flags.

	Attributes:
		set_flag_function (Callable[[FlagDefinition, Any], None]): Function to set a single flag.
		remove_flag_function (Callable[[str], None]): Function to remove a flag by its name.
		set_flags_function (Callable[[dict[str, Any]], None]): Function to set a dictionary of flags, overwriting existing ones.
		update_flags_function (Callable[[dict[str, Any]], None]): Function to update a dictionary of flags, merging with existing ones.
		clear_flags_function (Callable[..., None]): Function to clear all flags of this type.
		build_options_function (Callable[[Any], Any]): Function to build WebDriver options for this flag type.
		build_start_args_function (Callable[..., list[str]]): Function to build startup arguments for this flag type.
	"""
	
	set_flag_function: Callable[[FlagDefinition, Any], None]
	remove_flag_function: Callable[[str], None]
	set_flags_function: Callable[[dict[str, Any]], None]
	update_flags_function: Callable[[dict[str, Any]], None]
	clear_flags_function: Callable[..., None]
	build_options_function: Callable[["_any_webdriver_option_type"], "_any_webdriver_option_type"]
	build_start_args_function: Callable[..., list[str]]


class FlagNotDefined:
	"""A sentinel class to indicate that a flag definition was not found."""
	
	pass


AutoplayPolicyType = Literal["user-gesture-required", "no-user-gesture-required"]
ValidAutoplayPolicies = ["user-gesture-required", "no-user-gesture-required"]
LogLevelType = Literal[0, 1, 2, 3]
ValidLogLevels = [0, 1, 2, 3]
UseGLType = Literal["desktop", "egl", "swiftshader"]
ValidUseGLs = ["desktop", "egl", "swiftshader"]
_any_flags_mapping = Mapping[str, Any]
_any_webdriver_option_type = Union[
	webdriver.ChromeOptions,
	webdriver.EdgeOptions,
	webdriver.FirefoxOptions
]
_blink_webdriver_option_type = Union[webdriver.ChromeOptions, webdriver.EdgeOptions]
