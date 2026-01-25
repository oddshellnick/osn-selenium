from abc import ABC
from osn_selenium.abstract.webdriver.chrome import (
	AbstractChromeWebDriver
)


__all__ = ["AbstractYandexWebDriver"]


class AbstractYandexWebDriver(AbstractChromeWebDriver, ABC):
	"""
	Abstract composite class representing a full Yandex WebDriver.

	Combines lifecycle, settings, and base functionality for Yandex browser.
	Serves as the main entry point for abstract Yandex implementations.
	"""
	
	pass
