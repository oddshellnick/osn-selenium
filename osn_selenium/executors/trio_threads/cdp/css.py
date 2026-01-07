from osn_selenium.abstract.executors.cdp.css import (
	AbstractCssCDPExecutor
)
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)


class CssCDPExecutor(AbstractCssCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_rule(
			self,
			style_sheet_id: str,
			rule_text: str,
			location: Any,
			node_for_property_syntax_validation: Optional[int] = None
	) -> Any:
		return await self._execute_function("CSS.addRule", locals())
	
	async def collect_class_names(self, style_sheet_id: str) -> List[str]:
		return await self._execute_function("CSS.collectClassNames", locals())
	
	async def create_style_sheet(self, frame_id: str, force: Optional[bool] = None) -> str:
		return await self._execute_function("CSS.createStyleSheet", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("CSS.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("CSS.enable", locals())
	
	async def force_pseudo_state(self, node_id: int, forced_pseudo_classes: List[str]) -> None:
		return await self._execute_function("CSS.forcePseudoState", locals())
	
	async def force_starting_style(self, node_id: int, forced: bool) -> None:
		return await self._execute_function("CSS.forceStartingStyle", locals())
	
	async def get_animated_styles_for_node(self, node_id: int) -> Tuple[Optional[List[Any]]]:
		return await self._execute_function("CSS.getAnimatedStylesForNode", locals())
	
	async def get_background_colors(self, node_id: int) -> Tuple[Optional[List[str]]]:
		return await self._execute_function("CSS.getBackgroundColors", locals())
	
	async def get_computed_style_for_node(self, node_id: int) -> Tuple[List[Any]]:
		return await self._execute_function("CSS.getComputedStyleForNode", locals())
	
	async def get_environment_variables(self) -> dict:
		return await self._execute_function("CSS.getEnvironmentVariables", locals())
	
	async def get_inline_styles_for_node(self, node_id: int) -> Tuple[Optional[List[Any]]]:
		return await self._execute_function("CSS.getInlineStylesForNode", locals())
	
	async def get_layers_for_node(self, node_id: int) -> Any:
		return await self._execute_function("CSS.getLayersForNode", locals())
	
	async def get_location_for_selector(self, style_sheet_id: str, selector_text: str) -> List[Any]:
		return await self._execute_function("CSS.getLocationForSelector", locals())
	
	async def get_longhand_properties(self, shorthand_name: str, value: str) -> List[Any]:
		return await self._execute_function("CSS.getLonghandProperties", locals())
	
	async def get_matched_styles_for_node(self, node_id: int) -> Tuple[Optional[List[Any]]]:
		return await self._execute_function("CSS.getMatchedStylesForNode", locals())
	
	async def get_media_queries(self) -> List[Any]:
		return await self._execute_function("CSS.getMediaQueries", locals())
	
	async def get_platform_fonts_for_node(self, node_id: int) -> List[Any]:
		return await self._execute_function("CSS.getPlatformFontsForNode", locals())
	
	async def get_style_sheet_text(self, style_sheet_id: str) -> str:
		return await self._execute_function("CSS.getStyleSheetText", locals())
	
	async def resolve_values(
			self,
			values: List[str],
			node_id: int,
			property_name: Optional[str] = None,
			pseudo_type: Optional[str] = None,
			pseudo_identifier: Optional[str] = None
	) -> List[str]:
		return await self._execute_function("CSS.resolveValues", locals())
	
	async def set_container_query_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return await self._execute_function("CSS.setContainerQueryText", locals())
	
	async def set_effective_property_value_for_node(self, node_id: int, property_name: str, value: str) -> None:
		return await self._execute_function("CSS.setEffectivePropertyValueForNode", locals())
	
	async def set_keyframe_key(self, style_sheet_id: str, range_: Any, key_text: str) -> Any:
		return await self._execute_function("CSS.setKeyframeKey", locals())
	
	async def set_local_fonts_enabled(self, enabled: bool) -> None:
		return await self._execute_function("CSS.setLocalFontsEnabled", locals())
	
	async def set_media_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return await self._execute_function("CSS.setMediaText", locals())
	
	async def set_property_rule_property_name(self, style_sheet_id: str, range_: Any, property_name: str) -> Any:
		return await self._execute_function("CSS.setPropertyRulePropertyName", locals())
	
	async def set_rule_selector(self, style_sheet_id: str, range_: Any, selector: str) -> List[Any]:
		return await self._execute_function("CSS.setRuleSelector", locals())
	
	async def set_scope_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return await self._execute_function("CSS.setScopeText", locals())
	
	async def set_style_sheet_text(self, style_sheet_id: str, text: str) -> Optional[str]:
		return await self._execute_function("CSS.setStyleSheetText", locals())
	
	async def set_style_texts(
			self,
			edits: List[Any],
			node_for_property_syntax_validation: Optional[int] = None
	) -> List[List[Any]]:
		return await self._execute_function("CSS.setStyleTexts", locals())
	
	async def set_supports_text(self, style_sheet_id: str, range_: Any, text: str) -> Any:
		return await self._execute_function("CSS.setSupportsText", locals())
	
	async def start_rule_usage_tracking(self) -> None:
		return await self._execute_function("CSS.startRuleUsageTracking", locals())
	
	async def stop_rule_usage_tracking(self) -> List[Any]:
		return await self._execute_function("CSS.stopRuleUsageTracking", locals())
	
	async def take_computed_style_updates(self) -> List[int]:
		return await self._execute_function("CSS.takeComputedStyleUpdates", locals())
	
	async def take_coverage_delta(self) -> Tuple[List[Any]]:
		return await self._execute_function("CSS.takeCoverageDelta", locals())
	
	async def track_computed_style_updates(self, properties_to_track: List[Any]) -> None:
		return await self._execute_function("CSS.trackComputedStyleUpdates", locals())
	
	async def track_computed_style_updates_for_node(self, node_id: Optional[int] = None) -> None:
		return await self._execute_function("CSS.trackComputedStyleUpdatesForNode", locals())
