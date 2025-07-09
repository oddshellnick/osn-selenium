from typing import (
	Callable,
	TYPE_CHECKING,
	TypedDict
)


if TYPE_CHECKING:
	from osn_selenium.webdrivers.BaseDriver.webdriver import BrowserWebDriver


class CaptchaWorkerSettings(TypedDict):
	"""
	Typed dictionary for defining a captcha worker.

	Attributes:
		name (str): A unique name for the captcha worker.
		check_func (Callable[["BrowserWebDriver"], bool]): A callable function that takes a
			`BrowserWebDriver` instance and returns `True` if a captcha is detected.
		solve_func (Callable[["BrowserWebDriver"], None]): A callable function that takes a
			`BrowserWebDriver` instance and attempts to solve the captcha.
	"""
	
	name: str
	check_func: Callable[["BrowserWebDriver"], bool]
	solve_func: Callable[["BrowserWebDriver"], None]
