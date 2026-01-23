from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedCssCDPExecutor"]


class UnifiedCssCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_rule_impl(
			self,
			style_sheet_id: str,
			rule_text: str,
			location: Dict[str, Any],
			node_for_property_syntax_validation: Optional[int] = None
	) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.addRule",
				{
					"style_sheet_id": style_sheet_id,
					"rule_text": rule_text,
					"location": location,
					"node_for_property_syntax_validation": node_for_property_syntax_validation
				}
		)
	
	def _collect_class_names_impl(self, style_sheet_id: str) -> List[str]:
		return self._execute_function("CSS.collectClassNames", {"style_sheet_id": style_sheet_id})
	
	def _create_style_sheet_impl(self, frame_id: str, force: Optional[bool] = None) -> str:
		return self._execute_function("CSS.createStyleSheet", {"frame_id": frame_id, "force": force})
	
	def _disable_impl(self) -> None:
		return self._execute_function("CSS.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("CSS.enable", {})
	
	def _force_pseudo_state_impl(self, node_id: int, forced_pseudo_classes: List[str]) -> None:
		return self._execute_function(
				"CSS.forcePseudoState",
				{"node_id": node_id, "forced_pseudo_classes": forced_pseudo_classes}
		)
	
	def _force_starting_style_impl(self, node_id: int, forced: bool) -> None:
		return self._execute_function("CSS.forceStartingStyle", {"node_id": node_id, "forced": forced})
	
	def _get_animated_styles_for_node_impl(self, node_id: int) -> Tuple[
		Optional[List[Dict[str, Any]]],
		Optional[Dict[str, Any]],
		Optional[List[Dict[str, Any]]]
	]:
		return self._execute_function("CSS.getAnimatedStylesForNode", {"node_id": node_id})
	
	def _get_background_colors_impl(self, node_id: int) -> Tuple[Optional[List[str]], Optional[str], Optional[str]]:
		return self._execute_function("CSS.getBackgroundColors", {"node_id": node_id})
	
	def _get_computed_style_for_node_impl(self, node_id: int) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
		return self._execute_function("CSS.getComputedStyleForNode", {"node_id": node_id})
	
	def _get_environment_variables_impl(self) -> Any:
		return self._execute_function("CSS.getEnvironmentVariables", {})
	
	def _get_inline_styles_for_node_impl(self, node_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
		return self._execute_function("CSS.getInlineStylesForNode", {"node_id": node_id})
	
	def _get_layers_for_node_impl(self, node_id: int) -> Dict[str, Any]:
		return self._execute_function("CSS.getLayersForNode", {"node_id": node_id})
	
	def _get_location_for_selector_impl(self, style_sheet_id: str, selector_text: str) -> List[Dict[str, Any]]:
		return self._execute_function(
				"CSS.getLocationForSelector",
				{"style_sheet_id": style_sheet_id, "selector_text": selector_text}
		)
	
	def _get_longhand_properties_impl(self, shorthand_name: str, value: str) -> List[Dict[str, Any]]:
		return self._execute_function(
				"CSS.getLonghandProperties",
				{"shorthand_name": shorthand_name, "value": value}
		)
	
	def _get_matched_styles_for_node_impl(self, node_id: int) -> Tuple[
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
		return self._execute_function("CSS.getMatchedStylesForNode", {"node_id": node_id})
	
	def _get_media_queries_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("CSS.getMediaQueries", {})
	
	def _get_platform_fonts_for_node_impl(self, node_id: int) -> List[Dict[str, Any]]:
		return self._execute_function("CSS.getPlatformFontsForNode", {"node_id": node_id})
	
	def _get_style_sheet_text_impl(self, style_sheet_id: str) -> str:
		return self._execute_function("CSS.getStyleSheetText", {"style_sheet_id": style_sheet_id})
	
	def _resolve_values_impl(
			self,
			values: List[str],
			node_id: int,
			property_name: Optional[str] = None,
			pseudo_type: Optional[str] = None,
			pseudo_identifier: Optional[str] = None
	) -> List[str]:
		return self._execute_function(
				"CSS.resolveValues",
				{
					"values": values,
					"node_id": node_id,
					"property_name": property_name,
					"pseudo_type": pseudo_type,
					"pseudo_identifier": pseudo_identifier
				}
		)
	
	def _set_container_query_text_impl(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setContainerQueryText",
				{"style_sheet_id": style_sheet_id, "range_": range_, "text": text}
		)
	
	def _set_effective_property_value_for_node_impl(self, node_id: int, property_name: str, value: str) -> None:
		return self._execute_function(
				"CSS.setEffectivePropertyValueForNode",
				{"node_id": node_id, "property_name": property_name, "value": value}
		)
	
	def _set_keyframe_key_impl(self, style_sheet_id: str, range_: Dict[str, Any], key_text: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setKeyframeKey",
				{
					"style_sheet_id": style_sheet_id,
					"range_": range_,
					"key_text": key_text
				}
		)
	
	def _set_local_fonts_enabled_impl(self, enabled: bool) -> None:
		return self._execute_function("CSS.setLocalFontsEnabled", {"enabled": enabled})
	
	def _set_media_text_impl(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setMediaText",
				{"style_sheet_id": style_sheet_id, "range_": range_, "text": text}
		)
	
	def _set_property_rule_property_name_impl(self, style_sheet_id: str, range_: Dict[str, Any], property_name: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setPropertyRulePropertyName",
				{
					"style_sheet_id": style_sheet_id,
					"range_": range_,
					"property_name": property_name
				}
		)
	
	def _set_rule_selector_impl(self, style_sheet_id: str, range_: Dict[str, Any], selector: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setRuleSelector",
				{
					"style_sheet_id": style_sheet_id,
					"range_": range_,
					"selector": selector
				}
		)
	
	def _set_scope_text_impl(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setScopeText",
				{"style_sheet_id": style_sheet_id, "range_": range_, "text": text}
		)
	
	def _set_style_sheet_text_impl(self, style_sheet_id: str, text: str) -> Optional[str]:
		return self._execute_function(
				"CSS.setStyleSheetText",
				{"style_sheet_id": style_sheet_id, "text": text}
		)
	
	def _set_style_texts_impl(
			self,
			edits: List[Dict[str, Any]],
			node_for_property_syntax_validation: Optional[int] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"CSS.setStyleTexts",
				{
					"edits": edits,
					"node_for_property_syntax_validation": node_for_property_syntax_validation
				}
		)
	
	def _set_supports_text_impl(self, style_sheet_id: str, range_: Dict[str, Any], text: str) -> Dict[str, Any]:
		return self._execute_function(
				"CSS.setSupportsText",
				{"style_sheet_id": style_sheet_id, "range_": range_, "text": text}
		)
	
	def _start_rule_usage_tracking_impl(self) -> None:
		return self._execute_function("CSS.startRuleUsageTracking", {})
	
	def _stop_rule_usage_tracking_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("CSS.stopRuleUsageTracking", {})
	
	def _take_computed_style_updates_impl(self) -> List[int]:
		return self._execute_function("CSS.takeComputedStyleUpdates", {})
	
	def _take_coverage_delta_impl(self) -> Tuple[List[Dict[str, Any]], float]:
		return self._execute_function("CSS.takeCoverageDelta", {})
	
	def _track_computed_style_updates_for_node_impl(self, node_id: Optional[int] = None) -> None:
		return self._execute_function("CSS.trackComputedStyleUpdatesForNode", {"node_id": node_id})
	
	def _track_computed_style_updates_impl(self, properties_to_track: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"CSS.trackComputedStyleUpdates",
				{"properties_to_track": properties_to_track}
		)
