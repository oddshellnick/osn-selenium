from osn_selenium.dev_tools.filters import TargetsFilters
from typing import (
	Any,
	Callable,
	Dict,
	Iterable,
	Literal,
	Optional,
	Sequence,
	Union
)
from osn_selenium.exceptions.configuration import (
	DuplicationError,
	NotExpectedTypeError,
	NotExpectedValueError
)


__all__ = [
	"validate_log_filter",
	"validate_target_event",
	"validate_target_event_filter",
	"validate_target_type",
	"validate_type_filter"
]


def validate_log_filter(
		filter_mode: Literal["include", "exclude"],
		log_filter: Optional[Union[str, Iterable[str]]]
) -> Callable[[str], bool]:
	"""
	Creates a callable filter function based on the specified filter mode and values.

	This function generates a lambda that can be used to check if a given log level
	or target type should be processed, based on whether the filter is set to
	"include" (only process items in the filter) or "exclude" (process all items
	except those in the filter).

	Args:
		filter_mode (Literal["include", "exclude"]): The mode of the filter.
			"include" means only items present in `log_filter` will pass.
			"exclude" means all items except those present in `log_filter` will pass.
		log_filter (Optional[Union[str, Iterable[str]]]):
			A single log filter item or an iterable of such items.
			If None:
				- In "include" mode, the generated filter will always return False (nothing is included).
				- In "exclude" mode, the generated filter will always return True (nothing is excluded).

	Returns:
		Callable[[str], bool]: A callable function that takes a single argument (e.g., a log level or target type)
			and returns True if it passes the filter, False otherwise.

	Raises:
		ConfigurationError: If `filter_mode` or 'log_filter' is invalid.

	EXAMPLES
	________
	>>> # Example 1: Include only "INFO" logs
	... info_only_filter = validate_log_filter("include", "INFO")
	... print(info_only_filter("INFO"))	# True
	... print(info_only_filter("ERROR"))   # False
	>>> # Example 2: Exclude "DEBUG" and "WARNING" logs
	... no_debug_warning_filter = validate_log_filter("exclude", ["DEBUG", "WARNING"])
	... print(no_debug_warning_filter("INFO"))	# True
	... print(no_debug_warning_filter("DEBUG"))   # False
	>>> # Example 3: No filter (exclude mode, so everything passes)
	... all_logs_filter = validate_log_filter("exclude", None)
	... print(all_logs_filter("INFO"))	 # True
	... print(all_logs_filter("ERROR"))	# True
	"""
	
	filter_mode_error = NotExpectedValueError(
			value_name="filter_mode",
			value=filter_mode,
			valid_values=["include", "exclude"]
	)
	log_filter_error = NotExpectedTypeError(
			value_name="log_filter",
			value=log_filter,
			valid_types=("str", "Iterable[str]", "None")
	)
	
	if log_filter is None:
		if filter_mode == "include":
			return lambda x: False
	
		if filter_mode == "exclude":
			return lambda x: True
	
		raise filter_mode_error
	
	if isinstance(log_filter, str):
		if filter_mode == "include":
			return lambda x: x == log_filter
	
		if filter_mode == "exclude":
			return lambda x: x != log_filter
	
		raise filter_mode_error
	
	if isinstance(log_filter, Iterable):
		if filter_mode == "include":
			return lambda x: x in log_filter
	
		if filter_mode == "exclude":
			return lambda x: x not in log_filter
	
		raise filter_mode_error
	
	raise log_filter_error


def validate_type_filter(
		type_: str,
		filter_mode: Literal["include", "exclude"],
		filter_instances: Any
):
	"""
	Validates a target type against a given filter mode and filter instances.

	This is a wrapper around `_validate_log_filter` specifically for target types.

	Args:
		type_ (str): The target type string to check (e.g., "page", "iframe").
		filter_mode (Literal["include", "exclude"]): The mode of the filter ("include" or "exclude").
		filter_instances (Any): The filter value(s) (e.g., a string or a sequence of strings).

	Returns:
		bool: True if the `type_` passes the filter, False otherwise.
	"""
	
	return validate_log_filter(filter_mode, filter_instances)(type_)


def validate_target_event_filter(filter_: Optional[Sequence[Dict[str, Any]]]) -> TargetsFilters:
	"""
	Validates and processes a raw dictionary-based event filter into a `TargetsFilters` object.

	Args:
		filter_ (Optional[List[Dict[str, Any]]]): A list of dictionary filters defining inclusion/exclusion rules.

	Returns:
		TargetsFilters: A processed object containing excluded and included types.

	Raises:
		ValueError: If duplicate types appear in both included and excluded lists.
	"""
	
	if filter_ is None:
		filter_ = []
	
	all_excluded_types = [
		type_filter["type"]
		for type_filter in filter_
		if type_filter.get("exclude", True)
		and type_filter.get("type", None) is not None
	]
	all_included_types = [
		type_filter["type"]
		for type_filter in filter_
		if not type_filter.get("exclude", True)
		and type_filter.get("type", None) is not None
	]
	
	if len(set(all_excluded_types) & set(all_included_types)) > 0:
		raise DuplicationError(
				value_name="Excluded and included types",
				duplicated_values=set(all_excluded_types) &
				set(all_included_types)
		)
	
	other_types = any(
			type_filter.get("type", None) is None
			and not type_filter.get("exclude", True)
			for type_filter in filter_
	)
	
	return TargetsFilters(
			excluded=all_excluded_types,
			included=all_included_types,
			entire=other_types,
	)


def validate_target_type(type_: str, filter_: TargetsFilters) -> bool:
	"""
	Checks if a target type is valid based on the provided filter configuration.

	Args:
		type_ (str): The target type to check.
		filter_ (TargetsFilters): The filter configuration containing included and excluded types.

	Returns:
		bool: True if the target type is valid according to the filter, False otherwise.
	"""
	
	if type_ in filter_.excluded:
		return False
	
	if type_ in filter_.included:
		return True
	
	return filter_.entire


def validate_target_event(event: Any, filter_: TargetsFilters) -> Optional[bool]:
	"""
	Validates a target event against the provided filter.

	Args:
		event (Any): The event object containing target information.
		filter_ (TargetsFilters): The filter to apply.

	Returns:
		Optional[bool]: True if the event target is valid, False otherwise, or None if validation cannot be determined.
	"""
	
	result = None
	
	if hasattr(event, "target_info") and hasattr(event.target_info, "type_"):
		result = validate_target_type(type_=event.target_info.type_, filter_=filter_)
	
	if hasattr(event, "type_"):
		result = validate_target_type(type_=event.type_, filter_=filter_)
	
	return result
