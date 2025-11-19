from typing import Union
from osn_selenium.webdrivers.protocols import (
	SyncWebDriver,
	TrioThreadWebDriver
)


__all__ = ["ANY_WEBDRIVER_PROTOCOL_TYPEHINT"]

ANY_WEBDRIVER_PROTOCOL_TYPEHINT = Union[SyncWebDriver, TrioThreadWebDriver]
