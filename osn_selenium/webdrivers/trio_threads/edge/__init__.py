from osn_selenium.abstract.webdriver.edge import (
	AbstractEdgeWebDriver
)
from osn_selenium.webdrivers.trio_threads.edge.lifecycle import EdgeLifecycleMixin


class EdgeWebDriver(EdgeLifecycleMixin, AbstractEdgeWebDriver):
	"""
	Concrete Edge WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	pass
