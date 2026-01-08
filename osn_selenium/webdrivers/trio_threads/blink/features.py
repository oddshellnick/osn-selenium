from typing import Any, Dict
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.features import (
	AbstractBlinkFeaturesMixin
)


class BlinkFeaturesMixin(BlinkBaseMixin, AbstractBlinkFeaturesMixin):
	@requires_driver
	async def get_issue_message(self) -> str:
		return await self._wrap_to_trio(self.driver.get_issue_message)
	
	@requires_driver
	async def launch_app(self, id: str) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.launch_app, id=id)
	
	@requires_driver
	async def set_permissions(self, name: str, value: str) -> None:
		return await self._wrap_to_trio(self.driver.set_permissions, name=name, value=value)
