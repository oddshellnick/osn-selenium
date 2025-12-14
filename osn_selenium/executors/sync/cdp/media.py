from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.media import (
	AbstractMediaCDPExecutor
)


class MediaCDPExecutor(AbstractMediaCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Media.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Media.enable", locals())
