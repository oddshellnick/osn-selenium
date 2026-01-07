from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.abstract.executors.cdp.cast import (
	AbstractCastCDPExecutor
)


class CastCDPExecutor(AbstractCastCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Cast.disable", locals())
	
	def enable(self, presentation_url: Optional[str] = None) -> None:
		return self._execute_function("Cast.enable", locals())
	
	def set_sink_to_use(self, sink_name: str) -> None:
		return self._execute_function("Cast.setSinkToUse", locals())
	
	def start_desktop_mirroring(self, sink_name: str) -> None:
		return self._execute_function("Cast.startDesktopMirroring", locals())
	
	def start_tab_mirroring(self, sink_name: str) -> None:
		return self._execute_function("Cast.startTabMirroring", locals())
	
	def stop_casting(self, sink_name: str) -> None:
		return self._execute_function("Cast.stopCasting", locals())
