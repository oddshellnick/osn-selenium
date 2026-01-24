import os
import pathlib
from typing import Literal, Type, Union
from selenium.webdriver.common.actions.key_input import KeyInput
from selenium.webdriver.common.actions.wheel_input import WheelInput
from selenium.webdriver.common.actions.pointer_input import PointerInput


__all__ = [
	"ARCHITECTURES_TYPEHINT",
	"DEVICES_TYPEHINT",
	"PATH_TYPEHINT",
	"TYPES_FOR_FLATTENING_TYPEHINT"
]

DEVICES_TYPEHINT = Union[PointerInput, KeyInput, WheelInput]
ARCHITECTURES_TYPEHINT = Literal["sync", "trio_threads"]
PATH_TYPEHINT = Union[str, bytes, pathlib.Path, os.PathLike]
TYPES_FOR_FLATTENING_TYPEHINT = Union[str, Type]
