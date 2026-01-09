from osn_selenium.webdrivers.sync.chrome.lifecycle import ChromeLifecycleMixin
from osn_selenium.abstract.webdriver.chrome import (
	AbstractChromeWebDriver
)


class ChromeWebDriver(ChromeLifecycleMixin, AbstractChromeWebDriver):
	"""
	Concrete Chrome WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	pass
