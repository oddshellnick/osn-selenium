from osn_selenium.webdrivers.sync.chrome.lifecycle import ChromeLifecycleMixin
from osn_selenium.abstract.webdriver.chrome import (
	AbstractChromeWebDriver
)


class ChromeWebDriver(ChromeLifecycleMixin, AbstractChromeWebDriver):
	pass
