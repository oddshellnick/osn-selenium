from osn_selenium.abstract.webdriver.edge import (
	AbstractEdgeWebDriver
)
from osn_selenium.webdrivers.trio_threads.edge.lifecycle import EdgeLifecycleMixin


class EdgeWebDriver(EdgeLifecycleMixin, AbstractEdgeWebDriver):
	pass
