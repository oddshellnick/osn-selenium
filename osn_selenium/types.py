from typing import Self, Union
from win32api import GetSystemMetrics
from pydantic import (
	BaseModel,
	ConfigDict,
	Field
)
from selenium.webdriver.common.actions.key_input import KeyInput
from selenium.webdriver.common.actions.wheel_input import WheelInput
from selenium.webdriver.common.actions.pointer_input import PointerInput


class DictModel(BaseModel):
	"""
	Base class for Pydantic models with a predefined configuration.

	This configuration enforces strict validation rules such as forbidding extra
	fields and stripping whitespace from string inputs.
	"""
	
	model_config = ConfigDict(
			populate_by_name=True,
			extra="forbid",
			use_enum_values=True,
			str_strip_whitespace=True,
			validate_assignment=True,
	)


class WindowRect(DictModel):
	"""
	Defines a window's geometry with default values relative to screen size.

	The default values position the window in the center of the screen,
	occupying a significant portion of it.

	Attributes:
		x (int): The x-coordinate of the window's top-left corner.
				 Defaults to 1/4 of the screen width.
		y (int): The y-coordinate of the window's top-left corner.
				 Defaults to 10% of the screen height.
		width (int): The width of the window. Defaults to 1/2 of the
					 screen width.
		height (int): The height of the window. Defaults to 80% of the
					  screen height.
	"""
	
	x: int = Field(default_factory=lambda: GetSystemMetrics(0) // 4)
	y: int = Field(default_factory=lambda: int(GetSystemMetrics(1) * 0.1))
	width: int = Field(default_factory=lambda: GetSystemMetrics(0) // 2)
	height: int = Field(default_factory=lambda: int(GetSystemMetrics(1) * 0.8))


class Size(DictModel):
	"""
	Represents a 2D size.

	Attributes:
		width (int): The width dimension.
		height (int): The height dimension.
	"""
	
	width: int
	height: int


class Rectangle(DictModel):
	"""
	Defines a rectangle by its top-left corner and dimensions.

	Attributes:
		x (int): The x-coordinate of the top-left corner.
		y (int): The y-coordinate of the top-left corner.
		width (int): The width of the rectangle.
		height (int): The height of the rectangle.
	"""
	
	x: int
	y: int
	width: int
	height: int


class Position(DictModel):
	"""
	Represents a 2D coordinate.

	Attributes:
		x (int): The x-coordinate.
		y (int): The y-coordinate.
	"""
	
	x: int
	y: int


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
		return f"Point(x={self.x}, y={self.y})"
	
	def __eq__(self, other: Self) -> bool:
		return self.x == other.x and self.y == other.y
	
	def __ne__(self, other: Self) -> bool:
		return not self.__eq__(other)


class JS_Scripts(DictModel):
	"""
	Represents a collection of JavaScript script snippets for use with WebDriver.

	Attributes:
		check_element_in_viewport (str): JS to check if element is in the viewport.
		get_document_scroll_size (str): JS to get total scrollable dimensions.
		get_element_css (str): JS to get computed CSS styles of an element.
		get_element_rect_in_viewport (str): JS to get element bounds in viewport.
		get_random_element_point_in_viewport (str): JS to get a random visible point in element.
		get_viewport_position (str): JS to get scroll position of viewport.
		get_viewport_rect (str): JS to get viewport scroll offset and dimensions.
		get_viewport_size (str): JS to get dimensions of the viewport.
		stop_window_loading (str): JS to stop the page from loading.
		open_new_tab (str): JS to open a new tab.
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


class ExtraDictModel(BaseModel):
	"""
	Base class for Pydantic models that allows extra fields.

	This configuration allows the model to accept fields that are not
	explicitly defined in the model's schema.
	"""
	
	model_config = ConfigDict(
			populate_by_name=True,
			extra="allow",
			use_enum_values=True,
			str_strip_whitespace=True,
			validate_assignment=True,
	)


DEVICES_TYPEHINT = Union[PointerInput, KeyInput, WheelInput]
