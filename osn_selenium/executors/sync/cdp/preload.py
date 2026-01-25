from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.preload import (
	UnifiedPreloadCDPExecutor
)
from osn_selenium.abstract.executors.cdp.preload import (
	AbstractPreloadCDPExecutor
)


__all__ = ["PreloadCDPExecutor"]


class PreloadCDPExecutor(UnifiedPreloadCDPExecutor, AbstractPreloadCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedPreloadCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
