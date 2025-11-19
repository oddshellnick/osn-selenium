from typing import Union

from selenium.webdriver.common.actions.key_input import KeyInput
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.wheel_input import WheelInput
from win32api import GetSystemMetrics

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


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


class Position(DictModel):
    """
    Represents a 2D coordinate.

    Attributes:
        x (int): The x-coordinate.
        y (int): The y-coordinate.
    """
    x: int
    y: int


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


DEVICES_TYPEHINT = Union[PointerInput, KeyInput, WheelInput]
