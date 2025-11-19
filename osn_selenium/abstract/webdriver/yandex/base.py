from abc import ABC
from osn_selenium.abstract.webdriver.chrome.base import (
	AbstractChromeBaseMixin
)


__all__ = ["AbstractYandexBaseMixin"]


class AbstractYandexBaseMixin(AbstractChromeBaseMixin, ABC):
	"""
	Abstract mixin defining the base interface for Yandex WebDriver.

	This class serves as a foundational component for Yandex WebDriver implementations,
	providing access to the underlying Selenium WebDriver instance.
	"""
	
	pass
