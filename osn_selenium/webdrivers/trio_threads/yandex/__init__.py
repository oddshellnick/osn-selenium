from osn_selenium.abstract.webdriver.yandex import (
	AbstractYandexWebDriver
)
from osn_selenium.webdrivers.trio_threads.yandex.lifecycle import YandexLifecycleMixin


class YandexWebDriver(YandexLifecycleMixin, AbstractYandexWebDriver):
	"""
	Concrete Yandex WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	pass
