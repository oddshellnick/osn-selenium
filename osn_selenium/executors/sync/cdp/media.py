from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.media import (
	UnifiedMediaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.media import (
	AbstractMediaCDPExecutor
)


__all__ = ["MediaCDPExecutor"]


class MediaCDPExecutor(UnifiedMediaCDPExecutor, AbstractMediaCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedMediaCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
