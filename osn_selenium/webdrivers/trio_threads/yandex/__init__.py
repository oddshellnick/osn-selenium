from osn_selenium.abstract.webdriver.yandex import (
	AbstractYandexWebDriver
)
from osn_selenium.webdrivers.trio_threads.yandex.lifecycle import YandexLifecycleMixin


class YandexWebDriver(YandexLifecycleMixin, AbstractYandexWebDriver):
	pass
