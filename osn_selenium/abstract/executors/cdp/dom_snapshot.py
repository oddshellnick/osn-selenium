from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractDomSnapshotCDPExecutor"]


class AbstractDomSnapshotCDPExecutor(ABC):
	@abstractmethod
	def capture_snapshot(
			self,
			computed_styles: List[str],
			include_paint_order: Optional[bool] = None,
			include_dom_rects: Optional[bool] = None,
			include_blended_background_colors: Optional[bool] = None,
			include_text_color_opacities: Optional[bool] = None
	) -> Tuple[List[Dict[str, Any]], List[str]]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_snapshot(
			self,
			computed_style_whitelist: List[str],
			include_event_listeners: Optional[bool] = None,
			include_paint_order: Optional[bool] = None,
			include_user_agent_shadow_tree: Optional[bool] = None
	) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
		...
