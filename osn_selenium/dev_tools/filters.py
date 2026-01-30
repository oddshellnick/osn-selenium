from pydantic import Field
from typing import List, Optional
from osn_selenium._base_models import DictModel


__all__ = ["TargetFilter", "TargetsFilters"]


class TargetsFilters(DictModel):
	"""
	Configuration model for filtering target types (inclusion/exclusion).

	Attributes:
		excluded (List[str]): List of target types to exclude.
		included (List[str]): List of target types to include.
		entire (bool): Default behavior if a type is not explicitly listed.
	"""
	
	excluded: List[str] = Field(default_factory=list)
	included: List[str] = Field(default_factory=list)
	
	entire: bool = False


class TargetFilter(DictModel):
	"""
	Dataclass to define a filter for discovering new browser targets.

	Used in `DevToolsSettings` to specify which types of targets (e.g., "page", "iframe")
	should be automatically attached to or excluded.

	Attributes:
		type_ (Optional[str]): The type of target to filter by (e.g., "page", "iframe").
			If None, this filter applies regardless of type. Aliased as 'type'.
		exclude (Optional[bool]): If True, targets matching `type_` will be excluded.
			If False or None, targets matching `type_` will be included.
	"""
	
	type_: Optional[str] = Field(default=None, alias="type")
	exclude: Optional[bool] = None
