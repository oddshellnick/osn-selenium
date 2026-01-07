from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.css import (
	AbstractCssCDPExecutor
)


class CssCDPExecutor(AbstractCssCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def add_rule(
			self,
			style_sheet_id: str,
			rule_text: str,
			location: Any,
			node_for_property_syntax_validation: Optional[int] = None
	) -> Any:
		return self._execute_function("CSS.addRule", locals())
	
	def collect_class_names(self, style_sheet_id: str) -> List[str]:
		return self._execute_function("CSS.collectClassNames", locals())
	
	def create_style_sheet(self, frame_id: str, force: Optional[bool] = None) -> str:
		return self._execute_function("CSS.createStyleSheet", locals())
	
	def disable(self) -> None:
		return self._execute_function("CSS.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("CSS.enable", locals())
	
	def force_pseudo_state(self, node_id: int, forced_pseudo_classes: List[str]) -> None:
		return self._execute_function("CSS.forcePseudoState", locals())
	
	def force_starting_style(self, node_id: int, forced: bool) -> None:
		return self._execute_function("CSS.forceStartingStyle", locals())
	
	def get_animated_styles_for_node(self, node_id: int) -> Tuple[Optional[List[Any]], Optional[Any], Optional[List[Any]]]:
		return self._execute_function("CSS.getAnimatedStylesForNode", locals())
	
	def get_background_colors(self, node_id: int) -> Tuple[Optional[List[str]], Optional[str], Optional[str]]:
		return self._execute_function("CSS.getBackgroundColors", locals())
	
	def get_computed_style_for_node(self, node_id: int) -> Tuple[List[Any], Any]:
		return self._execute_function("CSS.getComputedStyleForNode", locals())
	
	def get_environment_variables(self) -> dict:
		return self._execute_function("CSS.getEnvironmentVariables", locals())
	
	def get_inline_styles_for_node(self, node_id: int) -> Tuple[Optional[Any], Optional[Any]]:
		return self._execute_function("CSS.getInlineStylesForNode", locals())
	
	def get_layers_for_node(self, node_id: int) -> Any:
		return self._execute_function("CSS.getLayersForNode", locals())
	
	def get_location_for_selector(self, style_sheet_id: str, selector_text: str) -> List[Any]:
		return self._execute_function("CSS.getLocationForSelector", locals())
	
	def get_longhand_properties(self, shorthand_name: str, value: str) -> List[Any]:
		return self._execute_function("CSS.getLonghandProperties", locals())
	
	def get_matched_styles_for_node(self, node_id: int) -> Tuple[
		Optional[Any],
		Optional[Any],
		Optional[List[Any]],
		Optional[List[Any]],
		Optional[List[Any]],
		Optional[List[Any]],
		Optional[List[Any]],
		Optional[List[Any]],
		Optional[int],
		Optional[List[Any]],
		Optional[List[Any]],
		Optional[Any],
		Optional[int],
		Optional[List[Any]]
	]:
		return self._execute_function("CSS.getMatchedStylesForNode", locals())
	
	def get_media_queries(self) -> List[Any]:
		return self._execute_function("CSS.getMediaQueries", locals())
	
	def get_platform_fonts_for_node(self, node_id: int) -> List[Any]:
		return self._execute_function("CSS.getPlatformFontsForNode", locals())
	
	def get_style_sheet_text(self, style_sheet_id: str) -> str:
		return self._execute_function("CSS.getStyleSheetText", locals())
	
	def resolve_values(
			self,
			values: List[str],
			node_id: int,
			property_name: Optional[str] = None,
			pseudo_type: Optional[str] = None,
			pseudo_identifier: Optional[str] = None
	) -> List[str]:
		return self._execute_function("CSS.resolveValues", locals())
	
	def set_container_query_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return self._execute_function("CSS.setContainerQueryText", locals())
	
	def set_effective_property_value_for_node(self, node_id: int, property_name: str, value: str) -> None:
		return self._execute_function("CSS.setEffectivePropertyValueForNode", locals())
	
	def set_keyframe_key(self, style_sheet_id: str, range_: Any, key_text: str) -> Any:
		return self._execute_function("CSS.setKeyframeKey", locals())
	
	def set_local_fonts_enabled(self, enabled: bool) -> None:
		return self._execute_function("CSS.setLocalFontsEnabled", locals())
	
	def set_media_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return self._execute_function("CSS.setMediaText", locals())
	
	def set_property_rule_property_name(self, style_sheet_id: str, range_: Any, property_name: str) -> Any:
		return self._execute_function("CSS.setPropertyRulePropertyName", locals())
	
	def set_rule_selector(self, style_sheet_id: str, range_: Any, selector: str) -> Any:
		return self._execute_function("CSS.setRuleSelector", locals())
	
	def set_scope_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return self._execute_function("CSS.setScopeText", locals())
	
	def set_style_sheet_text(self, style_sheet_id: str, text: str) -> Optional[str]:
		return self._execute_function("CSS.setStyleSheetText", locals())
	
	def set_style_texts(
			self,
			edits: List[Any],
			node_for_property_syntax_validation: Optional[int] = None
	) -> List[Any]:
		return self._execute_function("CSS.setStyleTexts", locals())
	
	def set_supports_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return self._execute_function("CSS.setSupportsText", locals())
	
	def start_rule_usage_tracking(self) -> None:
		return self._execute_function("CSS.startRuleUsageTracking", locals())
	
	def stop_rule_usage_tracking(self) -> List[Any]:
		return self._execute_function("CSS.stopRuleUsageTracking", locals())
	
	def take_computed_style_updates(self) -> List[int]:
		return self._execute_function("CSS.takeComputedStyleUpdates", locals())
	
	def take_coverage_delta(self) -> Tuple[List[Any], float]:
		return self._execute_function("CSS.takeCoverageDelta", locals())
	
	def track_computed_style_updates(self, properties_to_track: List[Any]) -> None:
		return self._execute_function("CSS.trackComputedStyleUpdates", locals())
	
	def track_computed_style_updates_for_node(self, node_id: Optional[int] = None) -> None:
		return self._execute_function("CSS.trackComputedStyleUpdatesForNode", locals())
