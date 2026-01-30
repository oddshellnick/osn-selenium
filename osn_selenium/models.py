from typing import Self
from osn_selenium._base_models import DictModel


__all__ = ["Point", "Position", "Rectangle", "Size", "WindowRect"]


class WindowRect(DictModel):
	"""
	Defines a window's geometry with default values relative to screen size.

	The default values position the window in the center of the screen,
	occupying a significant portion of it.

	Attributes:
		x (int): The x-coordinate of the window's top-left corner. Defaults to 100.
		y (int): The y-coordinate of the window's top-left corner. Defaults to 100.
		width (int): The width of the window. Defaults to 400.
		height (int): The height of the window. Defaults to 400.
	"""
	
	x: int = 100
	y: int = 100
	width: int = 1024
	height: int = 768


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
