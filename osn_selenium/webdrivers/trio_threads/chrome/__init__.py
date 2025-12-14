from osn_selenium.abstract.webdriver.chrome import (
	AbstractChromeWebDriver
)
from osn_selenium.webdrivers.trio_threads.chrome.lifecycle import ChromeLifecycleMixin


class ChromeWebDriver(ChromeLifecycleMixin, AbstractChromeWebDriver):
	"""
	Concrete Chrome WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	pass
