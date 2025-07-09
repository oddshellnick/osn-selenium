import trio
import pathlib
import warnings
from random import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.fedcm import FedCM
from selenium.webdriver.common.fedcm.dialog import Dialog
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.actions.key_input import KeyInput
from osn_selenium.captcha_workers import (
	CaptchaWorkerSettings
)
from selenium.webdriver.common.print_page_options import PrintOptions
from osn_selenium.webdrivers.BaseDriver._utils import build_cdp_kwargs
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.dev_tools.manager import (
	DevTools,
	DevToolsSettings
)
from osn_selenium.types import (
	Position,
	Rectangle,
	Size,
	WindowRect
)
from osn_selenium.webdrivers.types import (
	ActionPoint,
	_any_flags_mapping
)
from typing import (
	Any,
	Literal,
	Optional,
	TYPE_CHECKING,
	Type,
	Union,
	cast
)
from selenium.webdriver.common.actions.wheel_input import (
	ScrollOrigin,
	WheelInput
)
from osn_selenium.webdrivers.BaseDriver.protocols import (
	TrioWebDriverWrapperProtocol
)
from osn_selenium.webdrivers.BaseDriver.trio_wrapper import (
	TrioBrowserWebDriverWrapper
)
from osn_selenium.webdrivers.BaseDriver.flags import (
	BrowserFlags,
	BrowserFlagsManager
)
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)
from osn_selenium.webdrivers._functions import (
	move_to_parts,
	read_js_scripts,
	scroll_to_parts,
	text_input_to_parts
)


if TYPE_CHECKING:
	from osn_selenium.webdrivers.Blink.flags import BlinkFlagsManager


class BrowserWebDriver:
	"""
	A base class for managing a Selenium WebDriver instance and browser interactions.

	This class provides common functionalities for controlling a web browser using Selenium,
	including action chains, JavaScript execution, element interactions, window management,
	and integration with Trio for asynchronous operations. It serves as a foundation
	for browser-specific WebDriver implementations.

	Attributes:
		_window_rect (Optional[WindowRect]): The desired window size and position settings.
		_js_scripts (dict[str, str]): A dictionary of pre-loaded JavaScript snippets for common tasks.
		_webdriver_path (str): The file path to the WebDriver executable (e.g., chromedriver.exe).
		_webdriver_flags_manager (Union[BrowserFlagsManager, BlinkFlagsManager]): An object
			responsible for managing browser-specific flags and options.
		_driver (Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]): The active
			Selenium WebDriver instance. This will be None until `start_webdriver` is called.
		_base_implicitly_wait (int): The default implicit wait time in seconds for element searches.
		_base_page_load_timeout (int): The default page load timeout in seconds.
		_base_script_timeout (int): The default script timeout in seconds.
		_captcha_workers (Sequence[CaptchaWorkerSettings]): A list of configured captcha worker settings.
		_is_active (bool): A flag indicating if the WebDriver instance is currently active and connected.
		trio_capacity_limiter (trio.CapacityLimiter): A Trio capacity limiter used to control the
			concurrency of synchronous WebDriver operations when called from an async context.
		dev_tools (DevTools): An interface for interacting with the browser's DevTools protocol.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[BrowserFlagsManager] = BrowserFlagsManager,
			flags: Optional[Union[BrowserFlags, _any_flags_mapping]] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Union[int, float] = 40,
			captcha_workers: Optional[list[CaptchaWorkerSettings]] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
	):
		"""
		Initializes the BrowserWebDriver instance.

		Args:
			webdriver_path (str): The file path to the WebDriver executable.
			flags_manager_type (Type[BrowserFlagsManager]): The type of
				flags manager to use (e.g., `BrowserFlagsManager` or `BlinkFlagsManager`).
				Defaults to `BrowserFlagsManager`.
			flags (Optional[Union[BrowserFlags, _any_flags_mapping]]): Initial browser flags/options
				to apply. Can be a `BrowserFlags` object or a Mapping. Defaults to None.
			implicitly_wait (int): The default implicit wait time in seconds for element searches.
				Defaults to 5.
			page_load_timeout (int): The default page load timeout in seconds. Defaults to 5.
			script_timeout (int): The default asynchronous script timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): The initial window size and position. If None,
				the browser's default window size will be used. Defaults to None.
			trio_tokens_limit (Union[int, float]): The maximum number of concurrent synchronous
				WebDriver operations allowed when using the Trio wrapper. Defaults to 40.
			captcha_workers (Optional[Sequence[CaptchaWorkerSettings]]): A list of dictionaries,
				each defining a captcha worker with a name, check function, and solve function.
				Defaults to an empty list.
			devtools_settings (Optional[DevToolsSettings]): Settings for the DevTools integration.
				Defaults to None.
		"""
		
		self._window_rect = window_rect
		self._js_scripts = read_js_scripts()
		self._webdriver_path = webdriver_path
		self._webdriver_flags_manager: Union[BrowserFlagsManager, "BlinkFlagsManager"] = flags_manager_type()
		self._driver: Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]] = None
		self._base_implicitly_wait = implicitly_wait
		self._base_page_load_timeout = page_load_timeout
		self._base_script_timeout = script_timeout
		
		self._captcha_workers = captcha_workers if captcha_workers is not None else []
		
		self._is_active = False
		self.trio_capacity_limiter = trio.CapacityLimiter(trio_tokens_limit)
		
		self.dev_tools = DevTools(self, devtools_settings)
		
		self.update_settings(flags=flags)
	
	def add_captcha_worker(self, captcha_worker: CaptchaWorkerSettings):
		"""
		Adds a new captcha worker to the list of active captcha workers.

		Args:
			captcha_worker (CaptchaWorkerSettings): A dictionary containing the name,
				check function, and solve function for the captcha worker.
		"""
		
		self._captcha_workers.append(captcha_worker)
	
	def add_cookie(self, cookie_dict: dict[str, Any]):
		"""
		Adds a single cookie to the current browser session.

		Args:
			cookie_dict (dict[str, Any]): A dictionary representing the cookie to add.
		"""
		
		return self._driver.add_cookie(cookie_dict=cookie_dict)
	
	def add_credential(self, credential: Credential):
		"""
		Adds a WebAuthn credential to the browser's virtual authenticator.

		Args:
			credential (Credential): The `Credential` object representing the WebAuthn credential.
		"""
		
		self._driver.add_credential(credential=credential)
	
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions):
		"""
		Adds a virtual authenticator to the browser for WebAuthn testing.

		Args:
			options (VirtualAuthenticatorOptions): The `VirtualAuthenticatorOptions` object
				specifying the properties of the virtual authenticator.
		"""
		
		self._driver.add_virtual_authenticator(options=options)
	
	def build_action_chains(
			self,
			duration: int = 250,
			devices: Optional[list[Union[PointerInput, KeyInput, WheelInput]]] = None
	) -> ActionChains:
		"""
		Builds and returns a new Selenium ActionChains instance.

		Initializes an ActionChains object associated with the current WebDriver instance (`self.driver`).
		Allows specifying the default pause duration between actions and custom input device sources.

		Args:
			duration (int): The default duration in milliseconds to pause between actions
				within the chain. Defaults to 250.
			devices (Optional[list[Union[PointerInput, KeyInput, WheelInput]]]): A list of
				specific input device sources (Pointer, Key, Wheel) to use for the actions.
				If None, default devices are used. Defaults to None.

		Returns:
			ActionChains: A new ActionChains instance configured with the specified driver,
				duration, and devices.
		"""
		
		return ActionChains(driver=self._driver, duration=duration, devices=devices)
	
	def build_hm_move_action(
			self,
			start_position: ActionPoint,
			end_position: ActionPoint,
			parent_action: Optional[ActionChains] = None,
			duration: int = 250,
			devices: Optional[list[Union[PointerInput, KeyInput, WheelInput]]] = None
	) -> ActionChains:
		"""
		Builds a human-like mouse move action sequence between two points.

		Simulates a more natural mouse movement by breaking the path into smaller segments with pauses,
		calculated by the external `move_to_parts` function. Adds the corresponding move-by-offset
		actions and pauses to an ActionChains sequence. Assumes the starting point of the cursor
		is implicitly handled or should be set prior to performing this chain.

		Args:
			start_position (ActionPoint): The starting coordinates (absolute or relative, depends on `move_to_parts` logic).
			end_position (ActionPoint): The target coordinates for the mouse cursor.
			parent_action (Optional[ActionChains]): An existing ActionChains instance to append actions to.
				If None, a new chain is created. Defaults to None.
			duration (int): The base duration (in milliseconds) used when creating a new ActionChains
				instance if `parent_action` is None. Total move time depends on `move_to_parts`. Defaults to 250.
			devices (Optional[list[Union[PointerInput, KeyInput, WheelInput]]]): Specific input devices
				if creating a new ActionChains instance. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (new or parent) with the human-like move sequence added.
						  Needs to be finalized with `.perform()`.
		"""
		
		if parent_action is None:
			action = self.build_action_chains(duration=duration, devices=devices)
		else:
			action = parent_action
		
		move_parts = move_to_parts(start_position=start_position, end_position=end_position)
		
		for part in move_parts:
			action.pause(part.duration * 0.001)
			action.move_by_offset(xoffset=part.offset.x, yoffset=part.offset.y)
		
		return action
	
	def execute_js_script(self, script: str, *args) -> Any:
		"""
		Executes a JavaScript script in the current browser context.

		Executes arbitrary JavaScript code within the currently loaded webpage. This allows for
		performing actions that are not directly supported by WebDriver commands, such as complex
		DOM manipulations or accessing browser APIs.

		Args:
			script (str): The JavaScript code to execute as a string.
			*args: Arguments to pass to the JavaScript script. These are accessible in the script as `arguments[0]`, `arguments[1]`, etc.

		Returns:
			Any: The result of the JavaScript execution. JavaScript return values are converted to Python types.
				For example, JavaScript objects become Python dictionaries, arrays become lists, and primitives are converted directly.
		"""
		
		return self._driver.execute_script(script, *args)
	
	def get_element_rect_in_viewport(self, element: WebElement) -> Rectangle:
		"""
		Gets the position and dimensions of an element relative to the viewport.

		Executes a predefined JavaScript snippet that calculates the element's bounding rectangle
		as seen in the current viewport.

		Args:
			element (WebElement): The Selenium WebElement whose rectangle is needed.

		Returns:
			Rectangle: A TypedDict containing the 'x', 'y', 'width', and 'height' of the element
					   relative to the viewport's top-left corner. 'x' and 'y' can be negative
					   if the element is partially scrolled out of view to the top or left.
		"""
		
		rect = self.execute_js_script(self._js_scripts["get_element_rect_in_viewport"], element)
		
		return Rectangle(
				x=int(rect["x"]),
				y=int(rect["y"]),
				width=int(rect["width"]),
				height=int(rect["height"])
		)
	
	def get_random_element_point_in_viewport(self, element: WebElement, step: int = 1) -> Optional[Position]:
		"""
		Calculates a random point within the visible portion of a given element in the viewport.

		Executes a predefined JavaScript snippet that determines the element's bounding box
		relative to the viewport, calculates the intersection of this box with the viewport,
		and then selects a random point within that intersection, potentially aligned to a grid defined by `step`.

		Args:
			element (WebElement): The Selenium WebElement to find a random point within.
			step (int): Defines the grid step for selecting the random point. The coordinates
				will be multiples of this step within the valid range. Defaults to 1 (any pixel).

		Returns:
			Position: A TypedDict containing the integer 'x' and 'y' coordinates of a random point
					  within the element's visible area in the viewport. Coordinates are relative
					  to the element's top-left corner (0,0).
		"""
		
		position = self.execute_js_script(self._js_scripts["get_random_element_point_in_viewport"], element, step)
		
		if position is not None:
			return Position(x=int(position["x"]), y=int(position["y"]))
		
		return None
	
	def get_random_element_point(self, element: WebElement) -> ActionPoint:
		"""
		Gets the coordinates of a random point within an element, relative to the viewport origin.

		Calculates a random point within the visible portion of the element relative to the
		element's own top-left corner. It then adds the element's top-left coordinates
		(relative to the viewport) to get the final coordinates of the random point,
		also relative to the viewport's top-left origin (0,0).

		Args:
			element (WebElement): The target element within which to find a random point.

		Returns:
			ActionPoint: An ActionPoint named tuple containing the 'x' and 'y' coordinates
						 of the random point within the element, relative to the viewport origin.
		"""
		
		point_in_viewport = self.get_random_element_point_in_viewport(element=element, step=1)
		element_viewport_pos = self.get_element_rect_in_viewport(element=element)
		
		x = int(element_viewport_pos["x"] + point_in_viewport["x"])
		y = int(element_viewport_pos["y"] + point_in_viewport["y"])
		
		return ActionPoint(x=x, y=y)
	
	def build_hm_move_to_element_action(
			self,
			start_position: ActionPoint,
			element: WebElement,
			parent_action: Optional[ActionChains] = None,
			duration: int = 250,
			devices: Optional[list[Union[PointerInput, KeyInput, WheelInput]]] = None
	) -> tuple[ActionChains, ActionPoint]:
		"""
		Builds a human-like mouse move action from a start point to a random point within a target element.

		Determines a random target point within the element's boundary relative to the viewport
		(using `get_random_element_point`) and then uses `build_hm_move_action` to create
		a human-like movement sequence to that point. Returns both the action chain and the
		calculated end point.

		Args:
			start_position (ActionPoint): The starting coordinates (relative to viewport) for the mouse movement.
			element (WebElement): The target element to move the mouse into.
			parent_action (Optional[ActionChains]): An existing ActionChains instance to append actions to.
													If None, a new chain is created. Defaults to None.
			duration (int): Base duration (in milliseconds) used when creating a new ActionChains
							instance if `parent_action` is None. Total move time depends on the
							`move_to_parts` calculation within `build_hm_move_action`. Defaults to 250.
			devices (Optional[list[Union[PointerInput, KeyInput, WheelInput]]]): Specific input devices
																				 to use if creating a new ActionChains
																				 instance. Defaults to None.

		Returns:
			Tuple[ActionChains, ActionPoint]: A tuple containing:

				- The ActionChains instance with the human-like move-to-element sequence added.
				  Needs to be finalized with `.perform()`.
				- The calculated end `ActionPoint` (relative to viewport) within the element that the
				  mouse path targets.
		"""
		
		end_position = self.get_random_element_point(element=element)
		
		return (
				self.build_hm_move_action(
						start_position=start_position,
						end_position=end_position,
						parent_action=parent_action,
						duration=duration,
						devices=devices
				),
				end_position
		)
	
	def get_viewport_size(self) -> Size:
		"""
		Gets the current dimensions (width and height) of the browser's viewport.

		Executes a predefined JavaScript snippet to retrieve the inner width and height
		of the window.

		Returns:
			Size: A TypedDict containing the 'width' and 'height' of the viewport in pixels.
		"""
		
		size = self.execute_js_script(self._js_scripts["get_viewport_size"])
		
		return Size(width=int(size["width"]), height=int(size["height"]))
	
	def build_hm_scroll_action(
			self,
			delta_x: int,
			delta_y: int,
			origin: Optional[ScrollOrigin] = None,
			parent_action: Optional[ActionChains] = None,
			duration: int = 250,
			devices: Optional[list[Union[PointerInput, KeyInput, WheelInput]]] = None
	) -> ActionChains:
		"""
		Builds a human-like scroll action sequence by breaking the scroll into smaller parts with pauses.

		This method simulates a more natural scroll compared to a direct jump. It calculates scroll segments
		using an external `scroll_to_parts` function and adds corresponding scroll actions and pauses
		to an ActionChains sequence. If no origin is provided, it defaults to scrolling from the
		bottom-right corner for positive deltas and top-left for negative deltas of the viewport.

		Args:
			delta_x (int): The total horizontal distance to scroll. Positive scrolls right, negative scrolls left.
			delta_y (int): The total vertical distance to scroll. Positive scrolls down, negative scrolls up.
			origin (Optional[ScrollOrigin]): The origin point for the scroll (viewport or element center).
				If None, defaults to a viewport corner based on scroll direction. Defaults to None.
			parent_action (Optional[ActionChains]): An existing ActionChains instance to append actions to.
				If None, a new chain is created. Defaults to None.
			duration (int): The base duration (in milliseconds) used when creating a new ActionChains
				instance if `parent_action` is None. This duration is *not* directly the total scroll time,
				which is determined by the sum of pauses from `scroll_to_parts`. Defaults to 250.
			devices (Optional[list[Union[PointerInput, KeyInput, WheelInput]]]): Specific input devices
				to use if creating a new ActionChains instance. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (new or parent) with the human-like scroll sequence added.
						  Needs to be finalized with `.perform()`.
		"""
		
		if parent_action is None:
			action = self.build_action_chains(duration=duration, devices=devices)
		else:
			action = parent_action
		
		if origin is None:
			viewport_size = self.get_viewport_size()
			origin_x = 0 if delta_x >= 0 else viewport_size["width"]
			origin_y = 0 if delta_y >= 0 else viewport_size["height"]
			origin = ScrollOrigin.from_viewport(origin_x, origin_y)
		
		start_position = ActionPoint(x=int(origin.x_offset), y=int(origin.y_offset))
		end_position = ActionPoint(x=int(origin.x_offset) + delta_x, y=int(origin.y_offset) + delta_y)
		
		scroll_parts = scroll_to_parts(start_position=start_position, end_position=end_position)
		
		for part in scroll_parts:
			action.pause(part.duration * 0.001)
			action.scroll_from_origin(scroll_origin=origin, delta_x=int(part.delta.x), delta_y=int(part.delta.y))
		
		return action
	
	def get_viewport_rect(self) -> Rectangle:
		"""
		Gets the position and dimensions of the viewport relative to the document origin.

		Combines the scroll position (top-left corner) and the viewport dimensions.
		Executes a predefined JavaScript snippet.

		Returns:
			Rectangle: A TypedDict where 'x' and 'y' represent the current scroll offsets
					   (window.pageXOffset, window.pageYOffset) and 'width' and 'height' represent
					   the viewport dimensions (window.innerWidth, window.innerHeight).
		"""
		
		rect = self.execute_js_script(self._js_scripts["get_viewport_rect"])
		
		return Rectangle(
				x=int(rect["x"]),
				y=int(rect["y"]),
				width=int(rect["width"]),
				height=int(rect["height"])
		)
	
	def build_hm_scroll_to_element_action(
			self,
			element: WebElement,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
			origin: Optional[ScrollOrigin] = None,
			parent_action: Optional[ActionChains] = None,
			duration: int = 250,
			devices: Optional[list[Union[PointerInput, KeyInput, WheelInput]]] = None
	) -> ActionChains:
		"""
		Builds a human-like scroll action to bring an element into view with optional offsets.

		Calculates the necessary scroll delta (dx, dy) to make the target element visible within the
		viewport, considering additional offset margins. It then uses `build_hm_scroll_action`
		to perform the scroll in a human-like manner.

		Args:
			element (WebElement): The target element to scroll into view.
			additional_lower_y_offset (int): Extra space (in pixels) to leave below the element within the viewport. Defaults to 0.
			additional_upper_y_offset (int): Extra space (in pixels) to leave above the element within the viewport. Defaults to 0.
			additional_right_x_offset (int): Extra space (in pixels) to leave to the right of the element within the viewport. Defaults to 0.
			additional_left_x_offset (int): Extra space (in pixels) to leave to the left of the element within the viewport. Defaults to 0.
			origin (Optional[ScrollOrigin]): The origin point for the scroll. Passed to `build_hm_scroll_action`. Defaults to None.
			parent_action (Optional[ActionChains]): An existing ActionChains instance. Passed to `build_hm_scroll_action`. Defaults to None.
			duration (int): Base duration for creating a new ActionChains instance. Passed to `build_hm_scroll_action`. Defaults to 250.
			devices (Optional[list[Union[PointerInput, KeyInput, WheelInput]]]): Specific input devices. Passed to `build_hm_scroll_action`. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance containing the human-like scroll-to-element sequence.
						  Needs to be finalized with `.perform()`.
		"""
		
		viewport_rect = self.get_viewport_rect()
		element_rect = self.get_element_rect_in_viewport(element)
		
		if element_rect["x"] < additional_left_x_offset:
			delta_x = int(element_rect["x"] - additional_left_x_offset)
		elif element_rect["x"] + element_rect["width"] > viewport_rect["width"] - additional_right_x_offset:
			delta_x = int(
					element_rect["x"] +
					element_rect["width"] -
					(viewport_rect["width"] - additional_right_x_offset)
			)
		else:
			delta_x = 0
		
		if element_rect["y"] < additional_upper_y_offset:
			delta_y = int(element_rect["y"] - additional_upper_y_offset)
		elif element_rect["y"] + element_rect["height"] > viewport_rect["height"] - additional_lower_y_offset:
			delta_y = int(
					element_rect["y"] +
					element_rect["height"] -
					(viewport_rect["height"] - additional_lower_y_offset)
			)
		else:
			delta_y = 0
		
		return self.build_hm_scroll_action(
				delta_x=delta_x,
				delta_y=delta_y,
				origin=origin,
				parent_action=parent_action,
				duration=duration,
				devices=devices
		)
	
	def build_hm_text_input_action(
			self,
			text: str,
			parent_action: Optional[ActionChains] = None,
			duration: int = 250,
			devices: Optional[list[Union[PointerInput, KeyInput, WheelInput]]] = None
	) -> ActionChains:
		"""
		Builds a human-like text input action sequence.

		Simulates typing by breaking the input text into smaller chunks with pauses between them,
		calculated by the external `text_input_to_parts` function. Adds the corresponding
		send_keys actions and pauses to an ActionChains sequence.

		Args:
			text (str): The text string to be typed.
			parent_action (Optional[ActionChains]): An existing ActionChains instance to append actions to.
				If None, a new chain is created. Defaults to None.
			duration (int): The base duration (in milliseconds) used when creating a new ActionChains
				instance if `parent_action` is None. Total input time depends on `text_input_to_parts`. Defaults to 250.
			devices (Optional[list[Union[PointerInput, KeyInput, WheelInput]]]): Specific input devices
				if creating a new ActionChains instance. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (new or parent) with the human-like text input sequence added.
						  Needs to be finalized with `.perform()`. Requires the target input element to have focus.
		"""
		
		if parent_action is None:
			action = self.build_action_chains(duration=duration, devices=devices)
		else:
			action = parent_action
		
		input_parts = text_input_to_parts(text)
		
		for part in input_parts:
			action.pause(part.duration * 0.001)
			action.send_keys(part.text)
		
		return action
	
	@property
	def captcha_workers(self) -> list[CaptchaWorkerSettings]:
		"""
		Gets the current list of configured captcha workers.

		Returns:
			list[CaptchaWorkerSettings]: A list containing the current captcha worker settings.
		"""
		
		return self._captcha_workers
	
	def check_captcha(self, check_all: bool = False) -> list[str]:
		"""
		Iterates through registered captcha workers to detect and solve captchas.

		For each registered captcha worker, it calls a `check_func` to determine
		if a captcha is present. If found, it then calls the associated `solve_func`
		to attempt to solve it and records the name of the solved captcha.
		The process stops after the first solved captcha unless `check_all` is True.

		Args:
			check_all (bool): If True, all registered captcha workers will be checked
				and solved if present. If False, the method stops after the first
				captcha is successfully detected and solved. Defaults to False.

		Returns:
			list[str]: A list of names of the captchas that were detected and for which
				the `solve_func` was executed. The list will contain at most one element
				if `check_all` is False.
		"""
		
		found_captchas = []
		
		for captcha_worker in self._captcha_workers:
			if captcha_worker["check_func"](self):
				captcha_worker["solve_func"](self)
				found_captchas.append(captcha_worker["name"])
		
				if not check_all:
					break
		
		return found_captchas
	
	def check_element_in_viewport(self, element: WebElement) -> bool:
		"""
		Checks if the specified web element is currently within the browser's viewport.

		Executes a predefined JavaScript snippet to determine the visibility status.

		Args:
			element (WebElement): The Selenium WebElement to check.

		Returns:
			bool: True if the element is at least partially within the viewport, False otherwise.
		"""
		
		return self.execute_js_script(self._js_scripts["check_element_in_viewport"], element)
	
	def click_action(
			self,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a click action. Clicks on the specified element or the current mouse position if no element is provided.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (Optional[WebElement]): The web element to click. If None, clicks at the
				current mouse cursor position. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the click action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.click(on_element=element)
		
		return action_chain
	
	def click_and_hold_action(
			self,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a click-and-hold action. Holds down the left mouse button on the specified element or the current mouse position.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (Optional[WebElement]): The web element to click and hold. If None, clicks
				and holds at the current mouse cursor position. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the click-and-hold action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.click_and_hold(on_element=element)
		
		return action_chain
	
	@property
	def windows_handles(self) -> list[str]:
		"""
		Gets the handles of all open windows.

		Returns a list of handles for all browser windows or tabs currently open and managed by the WebDriver.
		This is useful for iterating through or managing multiple windows in a browser session.

		Returns:
		   list[str]: A list of window handles. Each handle is a string identifier for an open window.
		"""
		
		return self._driver.window_handles
	
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		"""
		Retrieves a window handle string based on the provided identifier.

		If the identifier is already a string, it's assumed to be a valid handle and returned directly.
		If it's an integer, it's treated as an index into the list of currently open window handles.
		If it's None or not provided, the handle of the currently active window is returned.

		Args:
			window (Optional[Union[str, int]]): The identifier for the desired window handle.

				- str: Assumed to be the window handle itself.
				- int: Index into the list of window handles (self.driver.window_handles).
				- None: Get the handle of the currently focused window.

		Returns:
			str: The window handle string corresponding to the input identifier.
		"""
		
		if isinstance(window, str):
			return window
		elif isinstance(window, int):
			return self._driver.window_handles[window]
		else:
			return self._driver.current_window_handle
	
	def switch_to_window(self, window: Optional[Union[str, int]] = None):
		"""
		Switches the driver's focus to the specified browser window.

		Uses get_window_handle to resolve the target window identifier (handle string or index)
		before instructing the driver to switch. If no window identifier is provided,
		it effectively switches to the current window.

		Args:
			window (Optional[Union[str, int]]): The identifier of the window to switch to.
				Can be a window handle (string) or an index (int) in the list of window handles.
				If None, targets the current window handle.
		"""
		
		self._driver.switch_to.window(self.get_window_handle(window))
	
	@property
	def current_window_handle(self) -> str:
		"""
		Gets the current window handle.

		Retrieves the handle of the currently active browser window or tab. Window handles are unique identifiers
		used by WebDriver to distinguish between different browser windows.

		Returns:
			str: The current window handle.
		"""
		
		return self._driver.current_window_handle
	
	def close_window(self, window: Optional[Union[str, int]] = None):
		"""
		Closes the specified browser window and manages focus switching.

		Identifies the target window to close using get_window_handle. Switches to that window,
		closes it, and then switches focus back. If the closed window was the currently focused
		window, it switches focus to the last window in the remaining list. Otherwise, it switches
		back to the window that had focus before the close operation began.

		Args:
			window (Optional[Union[str, int]]): The identifier of the window to close.
				Can be a window handle (string), an index (int), or None to close the
				currently focused window.
		"""
		
		start_window_handle = self.current_window_handle
		close_window_handle = self.get_window_handle(window)
		
		is_current_closing = close_window_handle == start_window_handle
		
		if not is_current_closing:
			self.switch_to_window(close_window_handle)
		
		self._driver.close()
		
		if len(self.windows_handles) > 0:
			if is_current_closing:
				self.switch_to_window(-1)
			else:
				self.switch_to_window(start_window_handle)
	
	def close_all_windows(self):
		"""
		Closes all open windows.

		Iterates through all window handles and closes each window associated with the WebDriver instance.
		This effectively closes the entire browser session managed by the driver.
		"""
		
		for window in self.windows_handles:
			self.close_window(window)
	
	def execute_cdp_cmd(self, cmd: str, cmd_args: dict[str, Any]) -> Any:
		"""
		Executes a Chrome DevTools Protocol (CDP) command.

		This method allows direct interaction with the browser's underlying DevTools Protocol,
		enabling fine-grained control over browser behavior, network, page rendering, and more.

		Args:
			cmd (str): The name of the CDP command to execute (e.g., "Page.navigate", "Network.enable", "Emulation.setDeviceMetricsOverride").
			cmd_args (dict[str, Any]): A dictionary of arguments specific to the given CDP command.
				The structure and required keys depend on the `cmd` being executed, as defined
				by the Chrome DevTools Protocol specification.

		Returns:
			Any: The result of the CDP command execution. The type and structure of the
				returned value depend on the specific `cmd` and its defined return type
				in the CDP specification.
		"""
		
		return self._driver.execute_cdp_cmd(cmd=cmd, cmd_args=build_cdp_kwargs(**cmd_args))
	
	def cmd_activate_target(self, target_id: str,):
		"""
		Activates a specific browser target, bringing it to the foreground.

		This command makes the specified target (tab or window) the active one,
		similar to clicking on a tab in a browser.

		Args:
			target_id (str): The unique ID of the target to activate.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		self.execute_cdp_cmd(cmd="Target.activateTarget", cmd_args=cmd_args)
	
	def cmd_attach_to_browser_target(self) -> str:
		"""
		Attaches the DevTools session to the browser itself, not a specific tab or page.

		This allows for control over browser-wide features, such as managing browser contexts,
		extensions, or global network settings.

		Returns:
			str: The `sessionId` of the newly created DevTools session for the browser.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.attachToBrowserTarget", cmd_args=cmd_args)
	
	def cmd_attach_to_target(self, target_id: str, flatten: Optional[bool] = None,) -> str:
		"""
		Attaches the DevTools session to a specific browser target.

		Attaching allows you to send CDP commands and receive events for that specific target.
		This is typically done to control a specific tab or iframe.

		Args:
			target_id (str): The unique ID of the target to attach to.
			flatten (Optional[bool]): If True, all child targets (e.g., iframes within a page)
				will also be automatically attached. Defaults to False.

		Returns:
			str: The `sessionId` of the newly created DevTools session for this target.
				This session ID is used in subsequent CDP commands to specify which session
				the command applies to.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.attachToTarget", cmd_args=cmd_args)
	
	def cmd_close_target(self, target_id: str,) -> bool:
		"""
		Closes a specific browser target (tab or window).

		Args:
			target_id (str): The unique ID of the target to close.

		Returns:
			bool: True if the target was successfully closed, False otherwise.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.closeTarget", cmd_args=cmd_args)
	
	def cmd_create_browser_context(
			self,
			dispose_on_detach: Optional[bool] = None,
			proxy_server: Optional[str] = None,
			proxy_bypass_list: Optional[str] = None,
			origins_with_universal_network_access: Optional[list[str]] = None,
	) -> str:
		"""
		Sends a Chrome DevTools Protocol (CDP) command to create a new browser context.

		A browser context is an isolated environment, similar to an incognito window,
		where cookies, local storage, and other browser data are separate from
		the default context.

		Args:
			dispose_on_detach (Optional[bool]): If True, the browser context will be
				disposed of when the last target in it is detached.
			proxy_server (Optional[str]): Proxy server to use for the browser context
				(e.g., "http://localhost:8080").
			proxy_bypass_list (Optional[str]): Comma-separated list of hosts or IP addresses
				for which proxying should be bypassed.
			origins_with_universal_network_access (Optional[Sequence[str]]): A list of
				origins that are allowed to make network requests to any origin.

		Returns:
			str: The `browserContextId` of the newly created browser context.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.createBrowserContext", cmd_args=cmd_args)
	
	def cmd_create_target(
			self,
			url: str = "",
			left: Optional[int] = None,
			top: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
			window_state: Optional[Literal["normal", "minimized", "maximized", "fullscreen"]] = None,
			browser_context_id: Optional[str] = None,
			enable_begin_frame_control: Optional[bool] = None,
			new_window: Optional[bool] = None,
			background: Optional[bool] = None,
			for_tab: Optional[bool] = None,
			hidden: Optional[bool] = None,
	) -> str:
		"""
		Sends a Chrome DevTools Protocol (CDP) command to create a new browser target (tab or window).

		This method wraps the `Target.createTarget` CDP command, allowing for the creation
		of new browsing contexts with various configurations such as URL, dimensions,
		window state, and association with a specific browser context.

		Args:
			url (str): The URL to open in the new target. Defaults to an empty string,
				which typically opens a blank page.
			left (Optional[int]): The x-coordinate (left edge) of the new window/tab.
				Only applicable if `new_window` is True.
			top (Optional[int]): The y-coordinate (top edge) of the new window/tab.
				Only applicable if `new_window` is True.
			width (Optional[int]): The width of the new window/tab in pixels.
				Only applicable if `new_window` is True.
			height (Optional[int]): The height of the new window/tab in pixels.
				Only applicable if `new_window` is True.
			window_state (Optional[Literal["normal", "minimized", "maximized", "fullscreen"]]): The desired state of the new window.
				Only applicable if `new_window` is True.
			browser_context_id (Optional[str]): If specified, the new target will be
				created in the browser context with this ID. This is useful for
				incognito modes or separate user profiles.
			enable_begin_frame_control (Optional[bool]): Whether to enable BeginFrame control
				for the new target. This is an advanced feature for precise rendering control.
			new_window (Optional[bool]): If True, the target will be opened in a new browser window.
				If False or None, it will typically open as a new tab.
			background (Optional[bool]): If True, the new target will be opened in the background
				without immediately gaining focus.
			for_tab (Optional[bool]): If True, indicates that the target is intended to be a tab.
				This parameter is often used in conjunction with `new_window=False`.
			hidden (Optional[bool]): If True, the new target will be created but not immediately
				visible.

		Returns:
			str: The `targetId` of the newly created browser target. This ID is essential
				for interacting with the new target via other CDP commands.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.createTarget", cmd_args=cmd_args)
	
	def cmd_detach_from_target(self, session_id: Optional[str] = None, target_id: Optional[str] = None,):
		"""
		Detaches the DevTools session from a specific target.

		Detaching stops the ability to send CDP commands and receive events for that target
		via the specified session. Either `session_id` or `target_id` must be provided.

		Args:
			session_id (Optional[str]): The ID of the DevTools session to detach.
			target_id (Optional[str]): The ID of the target from which to detach.
				If `session_id` is not provided, this ID is used.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		self.execute_cdp_cmd(cmd="Target.detachFromTarget", cmd_args=cmd_args)
	
	def cmd_dispose_browser_context(self, browser_context_id: str,):
		"""
		Disposes of an existing browser context.

		This closes all targets (tabs/windows) associated with the specified browser context
		and clears all associated data (e.g., cookies, local storage).

		Args:
			browser_context_id (str): The ID of the browser context to dispose of.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		self.execute_cdp_cmd(cmd="Target.disposeBrowserContext", cmd_args=cmd_args)
	
	def cmd_expose_dev_tools_protocol(
			self,
			target_id: str,
			binding_name: Optional[str] = None,
			inherit_permissions: Optional[bool] = None,
	):
		"""
		Exposes the DevTools Protocol API to the JavaScript context of a target.

		This allows JavaScript running within the target to directly interact with
		the DevTools Protocol by calling methods like `DevTools.evaluate` or `DevTools.send`.

		Args:
			target_id (str): The unique ID of the target to expose the protocol to.
			binding_name (Optional[str]): The name of the global object that will be
				exposed in the target's JavaScript context (default is "DevTools").
			inherit_permissions (Optional[bool]): If True, the exposed protocol will
				inherit permissions from the current DevTools session.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		self.execute_cdp_cmd(cmd="Target.exposeDevToolsProtocol", cmd_args=cmd_args)
	
	def cmd_get_browser_contexts(self) -> list[str]:
		"""
		Retrieves a list of all existing browser context IDs.

		Returns:
			list[str]: A list of strings, where each string is the unique ID of a browser context.

		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.getBrowserContexts", cmd_args=cmd_args)
	
	def cmd_get_target_info(self, target_id: Optional[str] = None,) -> Any:
		"""
		Retrieves detailed information about a specific target.

		If `target_id` is not provided, it typically returns information about the
		current default target or the browser target if no specific target is active.

		Args:
			target_id (Optional[str]): The unique ID of the target to get information for.
				If None, information about the current or default target is returned.

		Returns:
			Any: The `TargetInfo` object.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.getTargetInfo", cmd_args=cmd_args)
	
	def cmd_get_targets(self, filter_: Optional[list[Any]] = None,) -> Any:
		"""
		Retrieves a list of all available browser targets.

		This command can optionally filter the returned targets by type or other criteria.

		Args:
			filter_ (Optional[Sequence[Any]]): A list of target types or other filter criteria
				to narrow down the results. For example, `["page", "iframe"]` to get only
				pages and iframes.

		Returns:
			Any: A list of `TargetInfo` objects.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		return self.execute_cdp_cmd(cmd="Target.getTargets", cmd_args=cmd_args)
	
	def cmd_send_message_to_target(
			self,
			message: str,
			session_id: Optional[str] = None,
			target_id: Optional[str] = None,
	):
		"""
		Sends a raw DevTools Protocol message to a specific target.

		This is a low-level command for sending arbitrary CDP messages.
		Either `session_id` or `target_id` must be provided.

		Args:
			message (str): The raw JSON string of the CDP message to send.
				This message should conform to the CDP message format (e.g., `{"id": 1, "method": "Page.reload", "params": {}}`).
			session_id (Optional[str]): The ID of the DevTools session to send the message through.
			target_id (Optional[str]): The ID of the target to send the message to.
				If `session_id` is not provided, this ID is used.
		"""
		
		cmd_args = locals()
		cmd_args.pop("self")
		
		self.execute_cdp_cmd(cmd="Target.sendMessageToTarget", cmd_args=cmd_args)
	
	def context_click_action(
			self,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a context-click (right-click) action. Performs the action on the specified element or the current mouse position.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (Optional[WebElement]): The web element to context-click. If None, performs
				the context-click at the current mouse cursor position. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the context-click action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.context_click(on_element=element)
		
		return action_chain
	
	@property
	def cookies(self) -> list[dict[str, Any]]:
		"""
		Gets all cookies visible to the current page.

		Returns:
			list[dict[str, Any]]: A list of dictionaries, where each dictionary represents a cookie.
		"""
		
		return self._driver.get_cookies()
	
	@property
	def current_url(self) -> str:
		"""
		Gets the current URL.

		Retrieves the URL of the current page loaded in the browser window under WebDriver control.

		Returns:
			str: The current URL of the webpage.
		"""
		
		return self._driver.current_url
	
	def delete_all_cookies(self):
		"""
		Deletes all cookies from the current session.
		"""
		
		self._driver.delete_all_cookies()
	
	def delete_cookie(self, name: str):
		"""
		Deletes a single cookie by its name from the current session.

		Args:
			name (str): The name of the cookie to delete.
		"""
		
		self._driver.delete_cookie(name=name)
	
	def delete_downloadable_files(self):
		"""
		Deletes all downloadable files.
		"""
		
		self._driver.delete_downloadable_files()
	
	def double_click_action(
			self,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a double-click action. Performs the action on the specified element or the current mouse position.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (Optional[WebElement]): The web element to double-click. If None, double-clicks
				at the current mouse cursor position. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the double-click action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.double_click(on_element=element)
		
		return action_chain
	
	def download_file(self, file_name: str, target_directory: pathlib.Path):
		"""
		Downloads a file from the browser.

		Args:
			file_name (str): The name of the file to download as it appears in the browser's download list.
			target_directory (pathlib.Path): The local directory where the file should be saved.
		"""
		
		return self._driver.download_file(file_name=file_name, target_directory=str(target_directory.resolve()))
	
	def drag_and_drop_action(
			self,
			source_element: WebElement,
			target_element: WebElement,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a drag-and-drop action from a source element to a target element.

		Combines click-and-hold on the source, move to the target, and release.
		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			source_element (WebElement): The element to click and hold (the start of the drag).
			target_element (WebElement): The element to move to and release over (the end of the drop).
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the drag-and-drop action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.drag_and_drop(source=source_element, target=target_element)
		
		return action_chain
	
	def drag_and_drop_by_offset_action(
			self,
			source_element: WebElement,
			xoffset: int,
			yoffset: int,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a drag-and-drop action from a source element by a given offset.

		Combines click-and-hold on the source, move by the offset, and release.
		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			source_element (WebElement): The element to click and hold (the start of the drag).
			xoffset (int): The horizontal distance to move the mouse.
			yoffset (int): The vertical distance to move the mouse.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the drag-and-drop by offset action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.drag_and_drop_by_offset(source=source_element, xoffset=xoffset, yoffset=yoffset)
		
		return action_chain
	
	@property
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]:
		"""
		Gets the underlying Selenium WebDriver instance associated with this object.

		This property provides direct access to the WebDriver object (e.g., Chrome, Edge, Firefox)
		that is being controlled, allowing for direct Selenium operations if needed.

		Returns:
			Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]:
				The active WebDriver instance, or None if no driver is currently set or active.
		"""
		
		return self._driver
	
	async def execute_async_js_script(self, script: str, *args) -> Any:
		"""
		Executes an asynchronous JavaScript script in the context of the current page.

		This method allows you to run JavaScript code that can perform asynchronous
		operations (e.g., fetch data, wait for elements). The script is executed
		with a callback function as its last argument, which must be called to
		signal the completion of the script and return a value.

		Args:
			script (str): The JavaScript code to execute. The script must call
				the provided callback function (which will be the last argument
				passed to the script) to signal completion and return a value.
				For example: `arguments[arguments.length - 1](result);`
			*args (Any): Variable-length arguments to be passed to the JavaScript script.
				These arguments will be available in the JavaScript context as `arguments[0]`,
				`arguments[1]`, etc., before the callback function.

		Returns:
			Any: The value returned by the JavaScript script via the callback function.
				The type depends on what the JavaScript script returns.
		"""
		
		self._driver.execute_async_script(script, *args)
	
	@property
	def fedcm(self) -> FedCM:
		"""
		Gets the FedCM (Federated Credential Management) interface.

		Returns:
			FedCM: An object providing methods to interact with the FedCM API in the browser.
		"""
		
		return self._driver.fedcm
	
	@property
	def fedcm_dialog(self) -> Dialog:
		"""
		Gets the FedCM dialog interface.

		Returns:
			Dialog: An object providing methods to interact with the FedCM dialog.
		"""
		
		return self._driver.dialog
	
	def set_script_timeout(self, script_timeout: float):
		"""
		Sets the script timeout for WebDriver operations.

		Configures the maximum time WebDriver will wait for an JavaScript
		script to complete its execution before timing out.

		Args:
			script_timeout (float): The script timeout value in seconds.
		"""
		
		self._driver.set_script_timeout(script_timeout)
	
	def set_implicitly_wait_timeout(self, implicitly_wait_timeout: float):
		"""
		Sets the implicit wait timeout for WebDriver element searches.

		Configures the implicit wait time, which is the maximum time WebDriver will wait
		when searching for elements before throwing a `NoSuchElementException`. This setting
		applies globally to all element searches for the duration of the WebDriver session.

		Args:
			implicitly_wait_timeout (float): The implicit wait timeout value in seconds.
		"""
		
		self._driver.implicitly_wait(implicitly_wait_timeout)
	
	def set_page_load_timeout(self, page_load_timeout: float):
		"""
		Sets the page load timeout for WebDriver operations.

		Defines the maximum time WebDriver will wait for a page to fully load before timing out
		and throwing a `TimeoutException`. This is useful to prevent tests from hanging indefinitely
		on slow-loading pages.

		Args:
			page_load_timeout (float): The page load timeout value in seconds.
		"""
		
		self._driver.set_page_load_timeout(page_load_timeout)
	
	def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	):
		"""
		Sets all three WebDriver timeouts: page load, implicit wait, and script timeout.

		Args:
			page_load_timeout (float): The page load timeout in seconds.
			implicit_wait_timeout (float): The implicit wait timeout in seconds.
			script_timeout (float): The script timeout in seconds.
		"""
		
		self.set_page_load_timeout(page_load_timeout)
		self.set_implicitly_wait_timeout(implicit_wait_timeout)
		self.set_script_timeout(script_timeout)
	
	def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	):
		"""
		Updates the WebDriver's timeout settings, adding a small random delay for human-like behavior.

		If temporary timeouts are provided, they are used; otherwise, the base timeouts are used.
		A random float between 0 and 1 is added to each timeout to simulate variability.

		Args:
			temp_implicitly_wait (Optional[float]): Temporary implicit wait time in seconds.
				If provided, overrides the base implicit wait for this update. Defaults to None.
			temp_page_load_timeout (Optional[float]): Temporary page load timeout in seconds.
				If provided, overrides the base page load timeout for this update. Defaults to None.
			temp_script_timeout (Optional[float]): Temporary script timeout in seconds.
				If provided, overrides the base script timeout for this update. Defaults to None.
		"""
		
		if temp_implicitly_wait:
			implicitly_wait = temp_implicitly_wait + random()
		else:
			implicitly_wait = self._base_implicitly_wait + random()
		
		if temp_page_load_timeout:
			page_load_timeout = temp_page_load_timeout + random()
		else:
			page_load_timeout = self._base_page_load_timeout + random()
		
		if temp_page_load_timeout:
			script_timeout = temp_script_timeout + random()
		else:
			script_timeout = self._base_script_timeout + random()
		
		self.set_driver_timeouts(
				page_load_timeout=page_load_timeout,
				implicit_wait_timeout=implicitly_wait,
				script_timeout=script_timeout,
		)
	
	def find_inner_web_element(
			self,
			parent_element: WebElement,
			by: str,
			value: str,
			temp_implicitly_wait: Optional[int] = None,
			temp_page_load_timeout: Optional[int] = None,
			temp_script_timeout: Optional[float] = None,
	) -> WebElement:
		"""
		Finds a single web element within another element.

		Searches for a specific web element that is a descendant of a given parent web element.
		This is useful for locating elements within a specific section or component of a webpage.

		Args:
			parent_element (WebElement): The parent web element to search within. The search is scoped to this element's descendants.
			by (str): Locator strategy to use for finding the element (e.g., By.ID, By.XPATH).
			value (str): Locator value. The actual string used by the locator strategy to find the element.
			temp_implicitly_wait (Optional[int]): Temporary implicit wait time in seconds for this operation. Overrides default if provided. Defaults to None.
			temp_page_load_timeout (Optional[int]): Temporary page load timeout in seconds for this operation. Overrides default if provided. Defaults to None.
			temp_script_timeout (Optional[int]): Temporary script timeout in seconds for this operation. Overrides default if provided. Defaults to None.

		Returns:
			WebElement: The found web element. If no element is found within the timeout, a `NoSuchElementException` is raised.
		"""
		
		self.update_times(
				temp_implicitly_wait=temp_implicitly_wait,
				temp_page_load_timeout=temp_page_load_timeout,
				temp_script_timeout=temp_script_timeout
		)
		return parent_element.find_element(by, value)
	
	def find_inner_web_elements(
			self,
			parent_element: WebElement,
			by: str,
			value: str,
			temp_implicitly_wait: Optional[int] = None,
			temp_page_load_timeout: Optional[int] = None,
			temp_script_timeout: Optional[float] = None,
	) -> list[WebElement]:
		"""
		Finds multiple web elements within another element.

		Searches for all web elements that match the given criteria and are descendants of a
		specified parent web element. Returns a list of all matching elements found within the parent.

		Args:
			parent_element (WebElement): The parent web element to search within. The search is limited to this element's children.
			by (str): Locator strategy to use (e.g., By.CLASS_NAME, By.CSS_SELECTOR).
			value (str): Locator value. Used in conjunction with the 'by' strategy to locate elements.
			temp_implicitly_wait (Optional[int]): Temporary implicit wait time in seconds for this operation. Defaults to None.
			temp_page_load_timeout (Optional[int]): Temporary page load timeout in seconds for this operation. Defaults to None.
			temp_script_timeout (Optional[int]): Temporary script timeout in seconds for this operation. Overrides default if provided. Defaults to None.

		Returns:
			list[WebElement]: A list of found web elements. Returns an empty list if no elements are found.
		"""
		
		self.update_times(
				temp_implicitly_wait=temp_implicitly_wait,
				temp_page_load_timeout=temp_page_load_timeout,
				temp_script_timeout=temp_script_timeout
		)
		return parent_element.find_elements(by, value)
	
	def find_web_element(
			self,
			by: str,
			value: str,
			temp_implicitly_wait: Optional[int] = None,
			temp_page_load_timeout: Optional[int] = None,
			temp_script_timeout: Optional[float] = None,
	) -> WebElement:
		"""
		Finds a single web element on the page.

		Searches the entire webpage DOM for the first web element that matches the specified locator
		strategy and value. Returns the found element or raises an exception if no element is found within the timeout.

		Args:
			by (str): Locator strategy to use (e.g., By.ID, By.NAME).
			value (str): Locator value. Used with the 'by' strategy to identify the element.
			temp_implicitly_wait (Optional[int]): Temporary implicit wait time in seconds for this operation. Defaults to None.
			temp_page_load_timeout (Optional[int]): Temporary page load timeout in seconds for this operation. Defaults to None.
			temp_script_timeout (Optional[int]): Temporary script timeout in seconds for this operation. Overrides default if provided. Defaults to None.

		Returns:
			WebElement: The found web element.
		"""
		
		self.update_times(
				temp_implicitly_wait=temp_implicitly_wait,
				temp_page_load_timeout=temp_page_load_timeout,
				temp_script_timeout=temp_script_timeout
		)
		return self._driver.find_element(by, value)
	
	def find_web_elements(
			self,
			by: str,
			value: str,
			temp_implicitly_wait: Optional[int] = None,
			temp_page_load_timeout: Optional[int] = None,
			temp_script_timeout: Optional[float] = None,
	) -> list[WebElement]:
		"""
		Finds multiple web elements on the page.

		Searches the entire webpage for all web elements that match the specified locator strategy and value.
		Returns a list containing all matching elements. If no elements are found, an empty list is returned.

		Args:
			by (str): Locator strategy (e.g., By.TAG_NAME, By.LINK_TEXT).
			value (str): Locator value. Used with the 'by' strategy to locate elements.
			temp_implicitly_wait (Optional[int]): Temporary implicit wait time in seconds for this operation. Defaults to None.
			temp_page_load_timeout (Optional[int]): Temporary page load timeout in seconds for this operation. Defaults to None.
			temp_script_timeout (Optional[int]): Temporary script timeout in seconds for this operation. Overrides default if provided. Defaults to None.

		Returns:
			list[WebElement]: A list of found web elements. Returns an empty list if no elements are found.
		"""
		
		self.update_times(
				temp_implicitly_wait=temp_implicitly_wait,
				temp_page_load_timeout=temp_page_load_timeout,
				temp_script_timeout=temp_script_timeout
		)
		return self._driver.find_elements(by, value)
	
	def fullscreen_window(self):
		"""
		Makes the current browser window full screen.
		"""
		
		self._driver.fullscreen_window()
	
	def get_cookie(self, name: str) -> Optional[dict[str, Any]]:
		"""
		Gets a single cookie by its name.

		Args:
			name (str): The name of the cookie to retrieve.

		Returns:
			Optional[dict[str, Any]]: A dictionary representing the cookie if found, otherwise None.
		"""
		
		return self._driver.get_cookie(name=name)
	
	def get_credentials(self) -> list[Credential]:
		"""
		Gets a list of all registered WebAuthn credentials.

		Returns:
			list[Credential]: A list of `Credential` objects.
		"""
		
		return self._driver.get_credentials()
	
	def get_document_scroll_size(self) -> Size:
		"""
		Gets the total scrollable dimensions of the HTML document.

		Executes a predefined JavaScript snippet to retrieve the document's scrollWidth
		and scrollHeight.

		Returns:
			Size: A TypedDict where 'width' represents the document's scrollWidth,
					   'height' represents the scrollHeight.
		"""
		
		size = self.execute_js_script(self._js_scripts["get_document_scroll_size"])
		
		return Size(width=int(size["width"]), height=int(size["height"]))
	
	def get_downloadable_files(self) -> list[str]:
		"""
		Gets a list of downloadable files.

		Returns:
			list[str]: A list of file names that are currently available for download.
		"""
		
		return self._driver.get_downloadable_files()
	
	def get_element_css_style(self, element: WebElement) -> dict[str, str]:
		"""
		Retrieves the computed CSS style of a WebElement.

		Uses JavaScript to get all computed CSS properties and their values for a given web element.
		Returns a dictionary where keys are CSS property names and values are their computed values.

		Args:
			element (WebElement): The WebElement for which to retrieve the CSS style.

		Returns:
			dict[str, str]: A dictionary of CSS property names and their computed values as strings.
		"""
		
		return self.execute_js_script(self._js_scripts["get_element_css"], element)
	
	def get_fedcm_dialog(
			self,
			ignored_exceptions: Any,
			timeout: int = 5,
			poll_frequency: float = 0.5
	) -> Dialog:
		"""
		Waits for and retrieves the FedCM dialog.

		Args:
			ignored_exceptions (Any): Exceptions to ignore while waiting for the dialog.
			timeout (int): The maximum time to wait for the dialog to appear, in seconds. Defaults to 5.
			poll_frequency (float): How often to check for the dialog's presence, in seconds. Defaults to 0.5.

		Returns:
			Dialog: The FedCM dialog object.
		"""
		
		return self._driver.fedcm_dialog(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions
		)
	
	def get_screenshot_as_base64(self) -> str:
		"""
		Gets the screenshot of the current page as a Base64 encoded string.

		Returns:
			str: A Base64 encoded string representing the screenshot.
		"""
		
		return self._driver.get_screenshot_as_base64()
	
	def get_screenshot_as_file(self, file_path: pathlib.Path) -> bool:
		"""
		Saves a screenshot of the current page to a specified file.

		Args:
			file_path (pathlib.Path): The path where the screenshot should be saved.

		Returns:
			bool: True if the screenshot was successfully saved, False otherwise.
		"""
		
		return self._driver.get_screenshot_as_file(filename=file_path)
	
	def get_screenshot_as_png(self) -> bytes:
		"""
		Gets the screenshot of the current page as a PNG image in bytes.

		Returns:
			bytes: The screenshot as PNG formatted bytes.
		"""
		
		return self._driver.get_screenshot_as_png()
	
	def get_vars_for_remote(self) -> RemoteConnection:
		"""
		Gets variables necessary to create a remote WebDriver instance.

		Provides the command executor and session ID of the current WebDriver instance.
		These are needed to re-establish a connection to the same browser session from a different WebDriver client,
		for example, in a distributed testing environment.

		Returns:
			RemoteConnection: The command executor (for establishing connection).
		"""
		
		return self._driver.command_executor
	
	def get_viewport_position(self) -> Position:
		"""
		Gets the current scroll position of the viewport relative to the document origin (0,0).

		Executes a predefined JavaScript snippet to retrieve window.scrollX and window.scrollY.

		Returns:
			Position: A TypedDict containing the 'x' (horizontal scroll offset) and
					  'y' (vertical scroll offset) of the viewport.
		"""
		
		position = self.execute_js_script(self._js_scripts["get_viewport_position"])
		
		return Position(x=int(position["x"]), y=int(position["y"]))
	
	def key_down_action(
			self,
			value: str,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a key down (press and hold) action for a specific modifier key.

		Sends the key press to the specified element or the currently focused element.
		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			value (str): The modifier key to press (e.g., Keys.CONTROL, Keys.SHIFT).
			element (Optional[WebElement]): The element to send the key press to. If None,
				sends to the currently focused element. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the key down action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.key_down(value=value, element=element)
		
		return action_chain
	
	def key_up_action(
			self,
			value: str,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a key up (release) action for a specific modifier key.

		Sends the key release to the specified element or the currently focused element.
		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action. Typically used after `key_down_action`.

		Args:
			value (str): The modifier key to release (e.g., Keys.CONTROL, Keys.SHIFT).
			element (Optional[WebElement]): The element to send the key release to. If None,
				sends to the currently focused element. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the key up action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.key_up(value=value, element=element)
		
		return action_chain
	
	def maximize_window(self):
		"""
		Maximizes the current browser window.
		"""
		
		self._driver.maximize_window()
	
	def minimize_window(self):
		"""
		Minimizes the current browser window.
		"""
		
		self._driver.minimize_window()
	
	def move_to_element_action(
			self,
			element: WebElement,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a move mouse cursor action to the specified web element.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (WebElement): The target web element to move the mouse to.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the move action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.move_to_element(element)
		
		return action_chain
	
	def move_to_element_with_offset_action(
			self,
			element: WebElement,
			xoffset: int,
			yoffset: int,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds an action to move the mouse cursor to an offset from the center of a specified element.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (WebElement): The target web element to base the offset from.
			xoffset (int): The horizontal offset from the element's center. Positive is right, negative is left.
			yoffset (int): The vertical offset from the element's center. Positive is down, negative is up.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the move-with-offset action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.move_to_element_with_offset(element, xoffset=xoffset, yoffset=yoffset)
		
		return action_chain
	
	def open_new_tab(self, link: str = ""):
		"""
		Opens a new tab with the given URL.

		Opens a new browser tab and optionally navigates it to a specified URL. If no URL is provided, a blank tab is opened.

		Args:
			link (str): URL to open in the new tab. If empty, opens a blank tab. Defaults to "".
		"""
		
		self.execute_js_script(self._js_scripts["open_new_tab"], link)
	
	@property
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		"""
		Gets the current screen orientation (LANDSCAPE or PORTRAIT).

		Returns:
			Literal["LANDSCAPE", "PORTRAIT"]: The current screen orientation.
		"""
		
		return self._driver.orientation
	
	@orientation.setter
	def orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]):
		"""
		Sets the screen orientation.

		Args:
			value (Literal["LANDSCAPE", "PORTRAIT"]): The desired screen orientation.
		"""
		
		self._driver.orientation = value
	
	@property
	def page_source(self) -> str:
		"""
		Gets the HTML source code of the current page.

		Returns:
			str: The HTML source code as a string.
		"""
		
		return self._driver.page_source
	
	def print_page(self, print_options: Optional[PrintOptions] = None) -> str:
		"""
		Prints the current page to PDF.

		Args:
			print_options (Optional[PrintOptions]): Options for printing the page (e.g., orientation, scale).

		Returns:
			str: A Base64 encoded string of the PDF document.
		"""
		
		return self._driver.print_page(print_options=print_options)
	
	@property
	def rect(self) -> WindowRect:
		"""
		Gets the window rectangle.

		Retrieves the current position and size of the browser window as a `WindowRect` object.
		This object contains the x and y coordinates of the window's top-left corner, as well as its width and height.

		Returns:
			WindowRect: The window rectangle object containing x, y, width, and height.
		"""
		
		window_rect = self._driver.get_window_rect()
		
		return WindowRect(
				window_rect["x"],
				window_rect["y"],
				window_rect["width"],
				window_rect["height"]
		)
	
	def refresh_webdriver(self):
		"""
		Refreshes the current page.

		Reloads the currently loaded webpage in the browser. This action fetches the latest version of the page from the server.
		"""
		
		self._driver.refresh()
	
	def release_action(
			self,
			element: Optional[WebElement] = None,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a release mouse button action. Releases the depressed left mouse button on the specified element or the current mouse position.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action. Typically used after a `click_and_hold_action`.

		Args:
			element (Optional[WebElement]): The web element on which to release the mouse button.
				If None, releases at the current mouse cursor position. Defaults to None.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the release action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.release(on_element=element)
		
		return action_chain
	
	def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]):
		"""
		Connects to an existing remote WebDriver session.

		This method establishes a connection to a remote Selenium WebDriver server and reuses an existing browser session of Browser.
		It allows you to control a browser instance that is already running remotely, given the command executor URL and session ID of that session.

		Args:
			command_executor (Union[str, RemoteConnection]): The URL of the remote WebDriver server or a `RemoteConnection` object.
		"""
		
		self._driver = webdriver.Remote(
				command_executor=command_executor,
				options=self._webdriver_flags_manager.options
		)
		
		self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_script_timeout
		)
	
	def remove_all_credentials(self):
		"""
		Removes all registered WebAuthn credentials from the browser's virtual authenticator.
		"""
		
		self._driver.remove_all_credentials()
	
	def remove_captcha_worker(self, name: str):
		"""
		Removes a captcha worker from the list by its name.

		The method iterates through the registered workers and removes the first one
		that matches the given name. If no worker with the specified name is found,
		no action is taken.

		Args:
			name (str): The name of the captcha worker to remove.
		"""
		
		for i, captcha_worker in enumerate(self._captcha_workers):
			if captcha_worker["name"] == name:
				self._captcha_workers.pop(i)
				break
	
	def remove_credential(self, credential_id: Union[str, bytearray]):
		"""
		Removes a specific WebAuthn credential by its ID.

		Args:
			credential_id (Union[str, bytearray]): The ID of the credential to remove.
		"""
		
		self._driver.remove_credential(credential_id=credential_id)
	
	def remove_virtual_authenticator(self):
		"""
		Removes the currently active virtual authenticator from the browser.
		"""
		
		self._driver.remove_virtual_authenticator()
	
	def reset_captcha_workers(self, captcha_workers: Optional[list[CaptchaWorkerSettings]] = None):
		"""
		Resets the list of captcha workers, optionally replacing it with a new sequence.

		If `captcha_workers` is provided, the internal list is set to this new sequence.
		If `captcha_workers` is None, the internal list is cleared.

		Args:
			captcha_workers (Optional[Sequence[CaptchaWorkerSettings]]): An optional
				sequence of `CaptchaWorkerSettings` to replace the current list of workers.
				Defaults to None, which clears the list.
		"""
		
		self._captcha_workers = captcha_workers if captcha_workers is not None else []
	
	def set_trio_tokens_limit(self, trio_tokens_limit: Union[int, float]):
		"""
		Updates the total number of tokens for the Trio capacity limiter.

		Args:
			trio_tokens_limit (Union[int, float]): The new total token limit. Use math.inf for unlimited.
		"""
		
		self.trio_capacity_limiter.total_tokens = trio_tokens_limit
	
	@property
	def is_active(self) -> bool:
		"""
		Checks if the WebDriver instance is currently active and connected.

		This property provides a way to determine the current status of the WebDriver.
		It reflects whether the WebDriver is initialized and considered operational.

		Returns:
			bool: True if the WebDriver is active, False otherwise.
		"""
		
		return self._is_active
	
	def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Union[int, float] = 40,
	):
		"""
		Resets all configurable browser settings to their default or specified values.

		This method resets various browser settings to the provided values. If no value
		is provided for certain settings, they are reset to their default states.
		This can only be done when the browser is not active.

		Args:
			flags (Optional[BrowserFlags]): A dictionary of flags to apply. If provided, existing flags are cleared and replaced. If None, all flags are cleared.
			window_rect (Optional[WindowRect]): Updates the window rectangle settings. Defaults to a new WindowRect().
			trio_tokens_limit (Union[int, float]): The total number of tokens for the Trio capacity limiter. Defaults to 40.
		"""
		
		if not self.is_active:
			if window_rect is None:
				window_rect = WindowRect()
		
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self.set_trio_tokens_limit(trio_tokens_limit)
			self._window_rect = window_rect
		else:
			warnings.warn("Browser is already running.")
	
	def _create_driver(self):
		"""
		Abstract method to create a WebDriver instance. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide browser-specific
		WebDriver instantiation logic (e.g., creating ChromeDriver, FirefoxDriver, etc.).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def update_settings(
			self,
			flags: Optional[Union[BrowserFlags, _any_flags_mapping]] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Updates various browser settings after initialization or selectively.

		This method allows for dynamic updating of browser settings. Only the settings
		provided (not None) will be updated.

		Args:
			flags (Optional[Union[BrowserFlags, _any_flags_mapping]]): A dictionary of flags to update. Existing flags will be overwritten, others remain.
			window_rect (Optional[WindowRect]): Update the window rectangle settings. Defaults to None (no change).
			trio_tokens_limit (Optional[Union[int, float]]): Update the Trio token limit. Defaults to None (no change).
		"""
		
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)
		
		if window_rect is not None:
			self._window_rect = window_rect
		
		if trio_tokens_limit is not None:
			self.set_trio_tokens_limit(trio_tokens_limit)
	
	def start_webdriver(
			self,
			flags: Optional[Union[BrowserFlags, _any_flags_mapping]] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Starts the WebDriver service and the browser session.

		Initializes and starts the WebDriver instance and the associated browser process.
		It first updates settings based on provided parameters (if the driver is not already running),
		and then creates the WebDriver client instance (`self.driver`).

		Args:
			flags (Optional[Union[BrowserFlags, _any_flags_mapping]]): Override flags for this start. Defaults to None (use current settings).
			window_rect (Optional[WindowRect]): Override window rectangle for this start. Defaults to None (use current setting).
			trio_tokens_limit (Optional[Union[int, float]]): Override Trio token limit for this start. Defaults to None (use current setting).
		"""
		
		if self._driver is None:
			self.update_settings(
					flags=flags,
					window_rect=window_rect,
					trio_tokens_limit=trio_tokens_limit,
			)
		
			self._create_driver()
	
	def close_webdriver(self):
		"""
		Closes the WebDriver instance and terminates the associated browser subprocess.

		Quits the current WebDriver session, closes all browser windows, and then forcefully terminates
		the browser process. This ensures a clean shutdown of the browser and WebDriver environment.
		"""
		
		if self._driver is not None:
			self._driver.quit()
			self._driver = None
	
	def restart_webdriver(
			self,
			flags: Optional[Union[BrowserFlags, _any_flags_mapping]] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Restarts the WebDriver and browser session gracefully.

		Performs a clean restart by first closing the existing WebDriver session and browser
		(using `close_webdriver`), and then initiating a new session (using `start_webdriver`)
		with potentially updated settings. If settings arguments are provided, they override
		the existing settings for the new session; otherwise, the current settings are used.

		Args:
			flags (Optional[Union[BrowserFlags, _any_flags_mapping]]): Override flags for the new session. Defaults to None (use current).
			window_rect (Optional[WindowRect]): Override window rectangle for the new session. Defaults to None (use current).
			trio_tokens_limit (Optional[Union[int, float]]): Override Trio token limit for the new session. Defaults to None (use current).
		"""
		
		self.close_webdriver()
		self.start_webdriver(
				flags=flags,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
		)
	
	def scroll_by_amount_action(
			self,
			delta_x: int,
			delta_y: int,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a scroll action to the current mouse position by the specified amounts.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			delta_x (int): The amount to scroll horizontally. Positive scrolls right, negative scrolls left.
			delta_y (int): The amount to scroll vertically. Positive scrolls down, negative scrolls up.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the scroll action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.scroll_by_amount(delta_x=delta_x, delta_y=delta_y)
		
		return action_chain
	
	def scroll_from_origin_action(
			self,
			origin: ScrollOrigin,
			delta_x: int,
			delta_y: int,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a scroll action relative to a specified origin (viewport or element center).

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			origin (ScrollOrigin): The origin point for the scroll. This object defines
				whether the scroll is relative to the viewport or an element's center.
				Use `ScrollOrigin.from_viewport()` or `ScrollOrigin.from_element()`.
			delta_x (int): The horizontal scroll amount. Positive scrolls right, negative left.
			delta_y (int): The vertical scroll amount. Positive scrolls down, negative up.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the scroll action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.scroll_from_origin(scroll_origin=origin, delta_x=delta_x, delta_y=delta_y)
		
		return action_chain
	
	def scroll_to_element_action(
			self,
			element: WebElement,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds an action to scroll the viewport until the specified element is in view.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (WebElement): The target web element to scroll into view.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the scroll-to-element action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.scroll_to_element(element)
		
		return action_chain
	
	def search_url(
			self,
			url: str,
			temp_implicitly_wait: Optional[int] = None,
			temp_page_load_timeout: Optional[int] = None
	):
		"""
		Opens a URL in the current browser session.

		Navigates the browser to a specified URL. This action loads the new webpage in the current browser window or tab.

		Args:
			url (str): The URL to open. Must be a valid web address (e.g., "https://www.example.com").
			temp_implicitly_wait (Optional[int]): Temporary implicit wait time in seconds for page load. Defaults to None.
			temp_page_load_timeout (Optional[int]): Temporary page load timeout in seconds for page load. Defaults to None.
		"""
		
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		self._driver.get(url)
	
	def send_keys_action(
			self,
			keys_to_send: str,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a send keys action to the currently focused element.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			keys_to_send (str): The sequence of keys to send.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the send keys action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.send_keys(keys_to_send)
		
		return action_chain
	
	def send_keys_to_element_action(
			self,
			element: WebElement,
			keys_to_send: str,
			duration: int = 250,
			action_chain: Optional[ActionChains] = None
	) -> ActionChains:
		"""
		Adds a send keys action specifically to the provided web element.

		If an existing ActionChains object is provided via `action_chain`, this action
		is appended to it. Otherwise, a new ActionChains object is created using
		`self.build_action_chains` with the specified duration before adding the action.

		Args:
			element (WebElement): The target web element to send keys to.
			keys_to_send (str): The sequence of keys to send.
			duration (int): The duration in milliseconds to use when creating a new
				ActionChains instance if `action_chain` is None. Defaults to 250.
			action_chain (Optional[ActionChains]): An existing ActionChains instance to append
				this action to. If None, a new chain is created. Defaults to None.

		Returns:
			ActionChains: The ActionChains instance (either the one passed in or a new one)
				with the send keys to element action added, allowing for method chaining.
		"""
		
		if action_chain is None:
			action_chain = self.build_action_chains(duration=duration)
		
		action_chain.send_keys_to_element(element, keys_to_send)
		
		return action_chain
	
	def set_captcha_worker(self, captcha_worker: CaptchaWorkerSettings):
		"""
		Adds a captcha worker configuration to the list of workers.

		Args:
			captcha_worker (CaptchaWorkerSettings): The captcha worker settings to add.
		"""
		
		self._captcha_workers.append(captcha_worker)
	
	def set_user_verified(self, verified: bool):
		"""
		Sets the user verification state for WebAuthn.

		This is typically used with virtual authenticators to simulate user verification.

		Args:
			verified (bool): True to set the user as verified, False otherwise.
		"""
		
		self._driver.set_user_verified(verified=verified)
	
	def set_window_rect(self, rect: WindowRect):
		"""
		Sets the browser window rectangle.

		Adjusts the position and size of the browser window to the specified rectangle. This can be used
		to manage window placement and dimensions for testing or display purposes.

		Args:
			rect (WindowRect): An object containing the desired window rectangle parameters (x, y, width, height).
		"""
		
		self._driver.set_window_rect(x=rect.x, y=rect.y, width=rect.width, height=rect.height)
	
	def stop_window_loading(self):
		"""
		Stops the current page loading.

		Interrupts the loading process of the current webpage. This can be useful when a page is taking too long
		to load or when you want to halt resource loading for performance testing or specific scenarios.
		"""
		
		self.execute_js_script(self._js_scripts["stop_window_loading"])
	
	@property
	def supports_fedcm(self) -> bool:
		"""
		Checks if the browser supports the Federated Credential Management (FedCM) API.

		Returns:
			bool: True if FedCM is supported, False otherwise.
		"""
		
		return self._driver.supports_fedcm
	
	def switch_to_frame(self, frame: Union[str, int, WebElement]):
		"""
		Switches the driver's focus to a frame.

		Changes the WebDriver's focus to a specific frame within the current page. Frames are often used to embed
		content from other sources within a webpage. After switching to a frame, all WebDriver commands will be
		directed to elements within that frame until focus is switched back.

		Args:
			frame (Union[str, int, WebElement]): Specifies the frame to switch to. Can be a frame name (str), index (int), or a WebElement representing the frame.
		"""
		
		self._driver.switch_to.frame(frame)
	
	def to_wrapper(self) -> TrioWebDriverWrapperProtocol:
		"""
		Creates a TrioBrowserWebDriverWrapper instance for asynchronous operations with Trio.

		Wraps the ...WebDriver instance in a TrioBrowserWebDriverWrapper, which allows for running WebDriver
		commands in a non-blocking manner within a Trio asynchronous context. This is essential for
		integrating Selenium WebDriver with asynchronous frameworks like Trio.

		Returns:
			TrioWebDriverWrapperProtocol: A TrioBrowserWebDriverWrapper instance wrapping this BrowserWebDriver.
		"""
		
		return cast(
				TrioWebDriverWrapperProtocol,
				TrioBrowserWebDriverWrapper(_webdriver=self)
		)
	
	@property
	def virtual_authenticator_id(self) -> Optional[str]:
		"""
		Gets the ID of the active virtual authenticator.

		Returns:
			Optional[str]: The ID of the virtual authenticator if one is active, otherwise None.
		"""
		
		return self._driver.virtual_authenticator_id
