from osn_selenium.models import Point


__all__ = [
	"MoveOffset",
	"MovePart",
	"MoveStep",
	"ScrollDelta",
	"ScrollPart",
	"TextInputPart"
]


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


class MoveStep:
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
