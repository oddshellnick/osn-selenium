import math
from typing import List
from copy import deepcopy
from random import randint
from osn_selenium.models import Point
from osn_selenium.instances._utils import (
	MoveOffset,
	MovePart,
	MoveStep,
	ScrollDelta,
	ScrollPart,
	TextInputPart
)


__all__ = ["move_to_parts", "scroll_to_parts", "text_input_to_parts"]


def text_input_to_parts(text: str) -> List[TextInputPart]:
	"""
	Breaks down a text string into smaller parts for simulating human-like typing.

	Generates a List of `TextInputPart` objects, where each part contains a character
	or sequence of characters and a calculated duration. The duration simulates pauses
	between key presses, with potentially longer pauses between different consecutive
	characters.

	Args:
		text (str): The input string to be broken down.

	Returns:
		List[TextInputPart]: A List of `TextInputPart` objects representing the sequence
							 of text segments and their associated durations for simulated typing.
	"""
	
	parts = []
	previous_sign = None
	
	for sign in text:
		if previous_sign is None or sign == previous_sign:
			parts.append(TextInputPart(text=sign, duration=randint(50, 70)))
		else:
			parts.append(TextInputPart(text=sign, duration=randint(100, 200)))
	
		previous_sign = sign
	
	return parts


def scroll_to_parts(start_position: Point, end_position: Point) -> List[ScrollPart]:
	"""
	Calculates a sequence of smaller scroll steps with durations for human-like scrolling.

	Simulates scrolling by generating a series of vertical steps followed by horizontal steps
	until the target coordinates are reached. Each step is represented by a `ScrollPart`
	containing the scroll delta for that step and a random duration.

	Args:
		start_position (Point): The starting conceptual scroll position.
		end_position (Point): The target conceptual scroll position.

	Returns:
		List[ScrollPart]: A List of `ScrollPart` objects representing the sequence of scroll
						  movements and their associated durations. The `delta` in each part
						  represents the scroll amount for that step, and the `point` represents
						  the conceptual position *after* applying that delta.
	"""
	
	parts = []
	
	current_position = deepcopy(start_position)
	
	if start_position.y != end_position.y:
		while current_position.y != end_position.y:
			offset = randint(5, 20)
	
			if start_position.y > end_position.y:
				offset *= -1
	
			if start_position.y < end_position.y:
				if current_position.y + offset > end_position.y:
					offset = end_position.y - current_position.y
			elif start_position.y > end_position.y:
				if current_position.y + offset < end_position.y:
					offset = end_position.y - current_position.y
	
			current_position.y += offset
			parts.append(
					ScrollPart(
							point=deepcopy(current_position),
							delta=ScrollDelta(x=0, y=offset),
							duration=randint(1, 4)
					)
			)
	
	if start_position.x != end_position.x:
		while current_position.x != end_position.x:
			offset = randint(5, 20)
	
			if start_position.x > end_position.x:
				offset *= -1
	
			if start_position.x <= end_position.x:
				if current_position.x + offset > end_position.x:
					offset = end_position.x - current_position.x
			elif start_position.x > end_position.x:
				if current_position.x + offset < end_position.x:
					offset = current_position.x - end_position.x
	
			current_position.x += offset
			parts.append(
					ScrollPart(
							point=deepcopy(current_position),
							delta=ScrollDelta(x=offset, y=0),
							duration=randint(1, 4)
					)
			)
	
	return parts


def move_to_parts(start_position: Point, end_position: Point) -> List[MovePart]:
	"""
	Calculates a sequence of smaller move steps with durations for human-like mouse movement.

	Generates a path between a start and end point that deviates slightly from a
	straight line using a sinusoidal function, simulating more natural mouse movement.
	The path is broken into segments, each represented by a `MovePart` object specifying
	the target point for that segment, the offset from the previous point, and a random duration.

	Args:
		start_position (Point): The starting coordinates for the movement.
		end_position (Point): The target coordinates for the movement.

	Returns:
		List[MovePart]: A List of `MovePart` objects representing the sequence of mouse
						movements and their associated durations. Each `MovePart` indicates
						the `point` to move to, the `offset` from the previous point,
						and the `duration` for that movement segment.
	"""
	
	def get_new_position():
		"""Calculates random horizontal and vertical amplitudes for deviation."""
		
		linear_progress = step.index / len(steps)
		
		deviation_x = step.amplitude_x * math.sin(linear_progress * 2 * math.pi)
		current_x_linear = start_position.x + (end_position.x - start_position.x) * linear_progress
		
		deviation_y = step.amplitude_y * math.cos(linear_progress * 2 * math.pi)
		current_y_linear = start_position.y + (end_position.y - start_position.y) * linear_progress
		
		return Point(
				x=int(current_x_linear + deviation_x),
				y=int(current_y_linear + deviation_y)
		)
	
	def get_amplitude():
		"""Generates a sequence of internal _MoveStep objects."""
		
		amplitude_x = randint(10, 20)
		amplitude_y = randint(10, 20)
		
		if start_position.x > end_position.x:
			amplitude_x *= -1
		
		if start_position.y > end_position.y:
			amplitude_y *= -1
		
		return amplitude_x, amplitude_y
	
	def calculate_steps():
		"""Calculates the target point for a move step, including sinusoidal deviation."""
		
		steps_ = []
		current_point = deepcopy(start_position)
		index = 0
		
		while current_point != end_position:
			amplitude_x, amplitude_y = get_amplitude()
			steps_.append(MoveStep(amplitude_x=amplitude_x, amplitude_y=amplitude_y, index=index))
		
			index += 1
		
			if start_position.x <= end_position.x:
				current_point.x += amplitude_x if current_point.x + amplitude_x <= end_position.x else end_position.x - current_point.x
			else:
				current_point.x += amplitude_x if current_point.x + amplitude_x >= end_position.x else end_position.x - current_point.x
		
			if start_position.y <= end_position.y:
				current_point.y += amplitude_y if current_point.y + amplitude_y <= end_position.y else end_position.y - current_point.y
			else:
				current_point.y += amplitude_y if current_point.y + amplitude_y >= end_position.y else end_position.y - current_point.y
		
		return steps_
	
	parts = []
	steps = calculate_steps()
	previous_position = deepcopy(start_position)
	
	for step in steps:
		new_position = get_new_position()
	
		if start_position.x <= end_position.x:
			new_position.x = int(new_position.x if new_position.x < end_position.x else end_position.x)
		else:
			new_position.x = int(new_position.x if new_position.x > end_position.x else end_position.x)
	
		if start_position.y <= end_position.y:
			new_position.y = int(new_position.y if new_position.y < end_position.y else end_position.y)
		else:
			new_position.y = int(new_position.y if new_position.y > end_position.y else end_position.y)
	
		parts.append(
				MovePart(
						point=new_position,
						offset=MoveOffset(
								x=new_position.x - previous_position.x,
								y=new_position.y - previous_position.y
						),
						duration=randint(1, 4)
				)
		)
	
		previous_position = deepcopy(new_position)
	
		if parts[-1].point == end_position:
			break
	
	if parts[-1].point != end_position:
		parts.append(
				MovePart(
						point=end_position,
						offset=MoveOffset(
								x=end_position.x - previous_position.x,
								y=end_position.y - previous_position.y
						),
						duration=randint(1, 4)
				)
		)
	
	return parts
