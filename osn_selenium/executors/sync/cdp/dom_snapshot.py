from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.dom_snapshot import (
	AbstractDomSnapshotCDPExecutor
)


class DomSnapshotCDPExecutor(AbstractDomSnapshotCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def capture_snapshot(
			self,
			computed_styles: List[str],
			include_paint_order: Optional[bool] = None,
			include_dom_rects: Optional[bool] = None,
			include_blended_background_colors: Optional[bool] = None,
			include_text_color_opacities: Optional[bool] = None
	) -> Tuple[List[Any], List[str]]:
		return self._execute_function("DOMSnapshot.captureSnapshot", locals())
	
	def disable(self) -> None:
		return self._execute_function("DOMSnapshot.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("DOMSnapshot.enable", locals())
	
	def get_snapshot(
			self,
			computed_style_whitelist: List[str],
			include_event_listeners: Optional[bool] = None,
			include_paint_order: Optional[bool] = None,
			include_user_agent_shadow_tree: Optional[bool] = None
	) -> Tuple[List[Any], List[Any], List[Any]]:
		return self._execute_function("DOMSnapshot.getSnapshot", locals())
