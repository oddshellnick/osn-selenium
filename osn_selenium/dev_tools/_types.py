from typing import (
	Awaitable,
	Callable,
	Literal,
	TYPE_CHECKING
)


if TYPE_CHECKING:
	from osn_selenium.dev_tools.manager import DevToolsTarget


devtools_background_func_type = Callable[["DevToolsTarget"], Awaitable[None]]
LogLevelsType = Literal[
	"INFO",
	"ERROR",
	"DEBUG",
	"WARNING",
	"RequestPaused",
	"AuthRequired",
	"Building Kwargs"
]
