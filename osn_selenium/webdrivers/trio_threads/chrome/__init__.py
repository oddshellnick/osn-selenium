from osn_selenium.abstract.webdriver.chrome import (
	AbstractChromeWebDriver
)
from osn_selenium.webdrivers.trio_threads.chrome.lifecycle import ChromeLifecycleMixin


class ChromeWebDriver(ChromeLifecycleMixin, AbstractChromeWebDriver):
	pass
