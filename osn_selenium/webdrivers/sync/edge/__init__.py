from osn_selenium.webdrivers.sync.edge.lifecycle import EdgeLifecycleMixin
from osn_selenium.abstract.webdriver.edge import (
	AbstractEdgeWebDriver
)


class EdgeWebDriver(EdgeLifecycleMixin, AbstractEdgeWebDriver):
	"""
	Concrete Edge WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	pass
