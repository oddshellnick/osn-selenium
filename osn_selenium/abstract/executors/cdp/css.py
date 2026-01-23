from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractCssCDPExecutor"]


class AbstractCssCDPExecutor(ABC):
	@abstractmethod
	def add_rule(
			self,
			style_sheet_id: str,
			rule_text: str,
			location: Dict[str, Any],
			node_for_property_syntax_validation: Optional[int] = None
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def collect_class_names(self, style_sheet_id: str) -> List[str]:
		...
	
	@abstractmethod
	def create_style_sheet(self, frame_id: str, force: Optional[bool] = None) -> str:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def force_pseudo_state(self, node_id: int, forced_pseudo_classes: List[str]) -> None:
		...
	
	@abstractmethod
	def force_starting_style(self, node_id: int, forced: bool) -> None:
		...
	
	@abstractmethod
	def get_animated_styles_for_node(self, node_id: int) -> Tuple[
		Optional[List[Dict[str, Any]]],
		Optional[Dict[str, Any]],
		Optional[List[Dict[str, Any]]]
	]:
		...
	
	@abstractmethod
	def get_background_colors(self, node_id: int) -> Tuple[Optional[List[str]], Optional[str], Optional[str]]:
		...
	
	@abstractmethod
	def get_computed_style_for_node(self, node_id: int) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_environment_variables(self) -> Any:
		...
	
	@abstractmethod
	def get_inline_styles_for_node(self, node_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def get_layers_for_node(self, node_id: int) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_location_for_selector(self, style_sheet_id: str, selector_text: str) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_longhand_properties(self, shorthand_name: str, value: str) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_matched_styles_for_node(self, node_id: int) -> Tuple[
		Optional[Dict[str, Any]],
		Optional[Dict[str, Any]],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[int],
		Optional[List[Dict[str, Any]]],
		Optional[List[Dict[str, Any]]],
		Optional[Dict[str, Any]],
		Optional[int],
		Optional[List[Dict[str, Any]]]
	]:
		...
	
	@abstractmethod
	def get_media_queries(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_platform_fonts_for_node(self, node_id: int) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_style_sheet_text(self, style_sheet_id: str) -> str:
		...
	
	@abstractmethod
	def resolve_values(
			self,
			values: List[str],
			node_id: int,
			property_name: Optional[str] = None,
			pseudo_type: Optional[str] = None,
			pseudo_identifier: Optional[str] = None
	) -> List[str]:
		...
	
	@abstractmethod
	def set_container_query_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def set_effective_property_value_for_node(self, node_id: int, property_name: str, value: str) -> None:
		...
	
	@abstractmethod
	def set_keyframe_key(self, style_sheet_id: str, range_: Dict[str, Any], key_text: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def set_local_fonts_enabled(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_media_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def set_property_rule_property_name(self, style_sheet_id: str, range_: Dict[str, Any], property_name: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def set_rule_selector(self, style_sheet_id: str, range_: Dict[str, Any], selector: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def set_scope_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def set_style_sheet_text(self, style_sheet_id: str, text: str) -> Optional[str]:
		...
	
	@abstractmethod
	def set_style_texts(
			self,
			edits: List[Dict[str, Any]],
			node_for_property_syntax_validation: Optional[int] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_supports_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def start_rule_usage_tracking(self) -> None:
		...
	
	@abstractmethod
	def stop_rule_usage_tracking(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def take_computed_style_updates(self) -> List[int]:
		...
	
	@abstractmethod
	def take_coverage_delta(self) -> Tuple[List[Dict[str, Any]], float]:
		...
	
	@abstractmethod
	def track_computed_style_updates(self, properties_to_track: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def track_computed_style_updates_for_node(self, node_id: Optional[int] = None) -> None:
		...
