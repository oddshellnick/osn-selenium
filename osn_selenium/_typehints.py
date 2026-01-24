from typing import Literal, Union
from selenium.webdriver.common.actions.key_input import KeyInput
from selenium.webdriver.common.actions.wheel_input import WheelInput
from selenium.webdriver.common.actions.pointer_input import PointerInput


__all__ = ["ARCHITECTURE_TYPEHINT", "DEVICES_TYPEHINT"]

DEVICES_TYPEHINT = Union[PointerInput, KeyInput, WheelInput]
ARCHITECTURE_TYPEHINT = Literal["sync", "trio_threads"]
