from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.css import (
	UnifiedCssCDPExecutor
)
from osn_selenium.abstract.executors.cdp.css import (
	AbstractCssCDPExecutor
)


__all__ = ["CssCDPExecutor"]


class CssCDPExecutor(UnifiedCssCDPExecutor, AbstractCssCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedCssCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_rule(
			self,
			style_sheet_id: str,
			rule_text: str,
			location: Dict[str, Any],
			node_for_property_syntax_validation: Optional[int] = None
	) -> Dict[str, Any]:
		return self._add_rule_impl(
				style_sheet_id=style_sheet_id,
				rule_text=rule_text,
				location=location,
				node_for_property_syntax_validation=node_for_property_syntax_validation
		)
	
	def collect_class_names(self, style_sheet_id: str) -> List[str]:
		return self._collect_class_names_impl(style_sheet_id=style_sheet_id)
	
	def create_style_sheet(self, frame_id: str, force: Optional[bool] = None) -> str:
		return self._create_style_sheet_impl(frame_id=frame_id, force=force)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def force_pseudo_state(self, node_id: int, forced_pseudo_classes: List[str]) -> None:
		return self._force_pseudo_state_impl(node_id=node_id, forced_pseudo_classes=forced_pseudo_classes)
	
	def force_starting_style(self, node_id: int, forced: bool) -> None:
		return self._force_starting_style_impl(node_id=node_id, forced=forced)
	
	def get_animated_styles_for_node(self, node_id: int) -> Tuple[
		Optional[List[Dict[str, Any]]],
		Optional[Dict[str, Any]],
		Optional[List[Dict[str, Any]]]
	]:
		return self._get_animated_styles_for_node_impl(node_id=node_id)
	
	def get_background_colors(self, node_id: int) -> Tuple[Optional[List[str]], Optional[str], Optional[str]]:
		return self._get_background_colors_impl(node_id=node_id)
	
	def get_computed_style_for_node(self, node_id: int) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
		return self._get_computed_style_for_node_impl(node_id=node_id)
	
	def get_environment_variables(self) -> Any:
		return self._get_environment_variables_impl()
	
	def get_inline_styles_for_node(self, node_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
		return self._get_inline_styles_for_node_impl(node_id=node_id)
	
	def get_layers_for_node(self, node_id: int) -> Dict[str, Any]:
		return self._get_layers_for_node_impl(node_id=node_id)
	
	def get_location_for_selector(self, style_sheet_id: str, selector_text: str) -> List[Dict[str, Any]]:
		return self._get_location_for_selector_impl(style_sheet_id=style_sheet_id, selector_text=selector_text)
	
	def get_longhand_properties(self, shorthand_name: str, value: str) -> List[Dict[str, Any]]:
		return self._get_longhand_properties_impl(shorthand_name=shorthand_name, value=value)
	
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
		return self._get_matched_styles_for_node_impl(node_id=node_id)
	
	def get_media_queries(self) -> List[Dict[str, Any]]:
		return self._get_media_queries_impl()
	
	def get_platform_fonts_for_node(self, node_id: int) -> List[Dict[str, Any]]:
		return self._get_platform_fonts_for_node_impl(node_id=node_id)
	
	def get_style_sheet_text(self, style_sheet_id: str) -> str:
		return self._get_style_sheet_text_impl(style_sheet_id=style_sheet_id)
	
	def resolve_values(
			self,
			values: List[str],
			node_id: int,
			property_name: Optional[str] = None,
			pseudo_type: Optional[str] = None,
			pseudo_identifier: Optional[str] = None
	) -> List[str]:
		return self._resolve_values_impl(
				values=values,
				node_id=node_id,
				property_name=property_name,
				pseudo_type=pseudo_type,
				pseudo_identifier=pseudo_identifier
		)
	
	def set_container_query_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._set_container_query_text_impl(style_sheet_id=style_sheet_id, range_=range_, text=text)
	
	def set_effective_property_value_for_node(self, node_id: int, property_name: str, value: str) -> None:
		return self._set_effective_property_value_for_node_impl(node_id=node_id, property_name=property_name, value=value)
	
	def set_keyframe_key(self, style_sheet_id: str, range_: Dict[str, Any], key_text: str) -> Dict[str, Any]:
		return self._set_keyframe_key_impl(style_sheet_id=style_sheet_id, range_=range_, key_text=key_text)
	
	def set_local_fonts_enabled(self, enabled: bool) -> None:
		return self._set_local_fonts_enabled_impl(enabled=enabled)
	
	def set_media_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._set_media_text_impl(style_sheet_id=style_sheet_id, range_=range_, text=text)
	
	def set_property_rule_property_name(self, style_sheet_id: str, range_: Dict[str, Any], property_name: str) -> Dict[str, Any]:
		return self._set_property_rule_property_name_impl(
				style_sheet_id=style_sheet_id,
				range_=range_,
				property_name=property_name
		)
	
	def set_rule_selector(self, style_sheet_id: str, range_: Dict[str, Any], selector: str) -> Dict[str, Any]:
		return self._set_rule_selector_impl(style_sheet_id=style_sheet_id, range_=range_, selector=selector)
	
	def set_scope_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._set_scope_text_impl(style_sheet_id=style_sheet_id, range_=range_, text=text)
	
	def set_style_sheet_text(self, style_sheet_id: str, text: str) -> Optional[str]:
		return self._set_style_sheet_text_impl(style_sheet_id=style_sheet_id, text=text)
	
	def set_style_texts(
			self,
			edits: List[Dict[str, Any]],
			node_for_property_syntax_validation: Optional[int] = None
	) -> List[Dict[str, Any]]:
		return self._set_style_texts_impl(
				edits=edits,
				node_for_property_syntax_validation=node_for_property_syntax_validation
		)
	
	def set_supports_text(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._set_supports_text_impl(style_sheet_id=style_sheet_id, range_=range_, text=text)
	
	def start_rule_usage_tracking(self) -> None:
		return self._start_rule_usage_tracking_impl()
	
	def stop_rule_usage_tracking(self) -> List[Dict[str, Any]]:
		return self._stop_rule_usage_tracking_impl()
	
	def take_computed_style_updates(self) -> List[int]:
		return self._take_computed_style_updates_impl()
	
	def take_coverage_delta(self) -> Tuple[List[Dict[str, Any]], float]:
		return self._take_coverage_delta_impl()
	
	def track_computed_style_updates(self, properties_to_track: List[Dict[str, Any]]) -> None:
		return self._track_computed_style_updates_impl(properties_to_track=properties_to_track)
	
	def track_computed_style_updates_for_node(self, node_id: Optional[int] = None) -> None:
		return self._track_computed_style_updates_for_node_impl(node_id=node_id)
