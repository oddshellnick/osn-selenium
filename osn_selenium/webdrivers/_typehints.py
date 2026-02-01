from typing import TYPE_CHECKING, Union
from osn_selenium.webdrivers.protocols import (
	SyncWebDriver,
	TrioBiDiWebDriver,
	TrioThreadWebDriver
)


__all__ = ["ANY_TRIO_WEBDRIVER_TYPEHINT", "ANY_WEBDRIVER_PROTOCOL_TYPEHINT"]

if TYPE_CHECKING:
	from osn_selenium.webdrivers.trio_threads.core import CoreWebDriver as TrioThreadsWebDriver
	from osn_selenium.webdrivers.trio_bidi.core import CoreWebDriver as TrioBidiWebDriver

ANY_WEBDRIVER_PROTOCOL_TYPEHINT = Union[SyncWebDriver, TrioThreadWebDriver, TrioBiDiWebDriver]
ANY_TRIO_WEBDRIVER_TYPEHINT = Union["TrioThreadsWebDriver", "TrioBidiWebDriver"]
