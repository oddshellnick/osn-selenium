from typing import (
	Any,
	List,
	Tuple,
	Union
)


NUMBER = Union[int, float]
RANDOM_NUMBER = Tuple[NUMBER, NUMBER]
NOISE = Union[NUMBER]

RANDOM_NOISE = Union[List[NOISE], RANDOM_NUMBER]
RANDOM_VALUE = Union[List[Any], RANDOM_NUMBER]
