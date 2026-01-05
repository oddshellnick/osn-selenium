from typing import (
    Any,
    Awaitable,
    Callable,
    Literal,
    TYPE_CHECKING,
)


if TYPE_CHECKING:
    from osn_selenium.dev_tools.target.base import BaseMixin as BaseTargetMixin
else:
    BaseTargetMixin = Any


devtools_background_func_type = Callable[
    [BaseTargetMixin],
    Awaitable[None]
]


LogLevelsType = Literal[
    "INFO",
    "ERROR",
    "DEBUG",
    "WARNING",
    "RequestPaused",
    "AuthRequired",
    "Building Kwargs"
]
