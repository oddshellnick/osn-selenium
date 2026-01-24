from typing import Union
from osn_selenium.webdrivers.protocols import (
	SyncWebDriver,
	TrioThreadWebDriver
)


__all__ = ["ANY_WEBDRIVER_PROTOCOL"]


ANY_WEBDRIVER_PROTOCOL = Union[SyncWebDriver, TrioThreadWebDriver]
