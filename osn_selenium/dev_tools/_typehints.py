from typing import (
	Any,
	Callable,
	Coroutine,
	Literal,
	TYPE_CHECKING,
	Union
)


__all__ = [
	"CDP_LOG_LEVELS_TYPEHINT",
	"DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT",
	"FINGERPRINT_LOG_LEVELS_TYPEHINT"
]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target.base import BaseMixin as BaseTargetMixin
	from osn_selenium.dev_tools.target import DevToolsTarget
else:
	BaseTargetMixin = Any
	DevToolsTarget = Any

DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT = Callable[[Union[BaseTargetMixin, DevToolsTarget]], Coroutine[Any, Any, None]]

CDP_LOG_LEVELS_TYPEHINT = Literal[
	"INFO",
	"ERROR",
	"DEBUG",
	"WARNING",
	"RequestPaused",
	"AuthRequired",
	"Building Kwargs"
]
FINGERPRINT_LOG_LEVELS_TYPEHINT = Literal["Detect"]
