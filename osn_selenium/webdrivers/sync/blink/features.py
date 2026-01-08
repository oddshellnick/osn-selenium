from typing import Any, Dict
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.features import (
	AbstractBlinkFeaturesMixin
)


class BlinkFeaturesMixin(BlinkBaseMixin, AbstractBlinkFeaturesMixin):
	@requires_driver
	def get_issue_message(self) -> Any:
		return self.driver.get_issue_message()
	
	@requires_driver
	def launch_app(self, id: str) -> Dict[str, Any]:
		return self.driver.launch_app(id=id)
	
	@requires_driver
	def set_permissions(self, name: str, value: str) -> None:
		self.driver.set_permissions(name=name, value=value)
