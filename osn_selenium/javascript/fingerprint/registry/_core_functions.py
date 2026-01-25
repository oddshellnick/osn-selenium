from typing import (
	Any,
	Dict,
	Iterable,
	Mapping,
	Optional
)
from osn_selenium.javascript.fingerprint.registry.models import RegistryItem
from osn_selenium.javascript.fingerprint.registry._typehints import ITEM_TYPE_TYPEHINT


__all__ = [
	"register",
	"register_key_methods",
	"register_keys_methods",
	"register_target_methods",
	"register_targets",
	"register_targets_methods"
]


def register(
		registry: Dict[str, RegistryItem],
		target: str,
		key: str,
		type_: ITEM_TYPE_TYPEHINT,
		api: str,
		method: Optional[str],
		settings: Optional[Dict[str, Any]] = None
) -> Dict[str, RegistryItem]:
	"""
	Registers a single item into the registry.

	Args:
		registry (Dict[str, RegistryItem]): The registry dictionary to update.
		target (str): The JavaScript target object/class.
		key (str): The unique key for the registry entry.
		type_ (ITEM_TYPE): The type of hook ('method', 'prop', 'constructor').
		api (str): The API category name.
		method (Optional[str]): The name of the method/property, or None.
		settings (Optional[Dict[str, Any]]): Additional configuration settings.

	Returns:
		Dict[str, RegistryItem]: The updated registry dictionary.
	"""
	
	registry[key] = RegistryItem(target=target, name=method, type=type_, api=api, settings=settings)
	
	return registry


def register_targets_methods(
		registry: Dict[str, RegistryItem],
		targets: Iterable[str],
		type_: ITEM_TYPE_TYPEHINT,
		api: str,
		methods: Iterable[str],
		settings: Optional[Dict[str, Any]] = None
) -> Dict[str, RegistryItem]:
	"""
	Registers multiple methods for multiple targets.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.
		targets (Iterable[str]): A list of target objects.
		type_ (ITEM_TYPE): The type of the items.
		api (str): The API category.
		methods (Iterable[str]): A list of methods to register for each target.
		settings (Optional[Dict[str, Any]]): Configuration settings.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	for target in targets:
		for method in methods:
			registry = register(
					registry=registry,
					key=f"{target}.{method}",
					target=target,
					type_=type_,
					api=api,
					method=method,
					settings=settings
			)
	
	return registry


def register_targets(
		registry: Dict[str, RegistryItem],
		targets: Iterable[str],
		type_: ITEM_TYPE_TYPEHINT,
		api: str,
		settings: Optional[Dict[str, Any]] = None
) -> Dict[str, RegistryItem]:
	"""
	Registers multiple targets directly without specific methods.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.
		targets (Iterable[str]): A list of target objects.
		type_ (ITEM_TYPE): The type of the items.
		api (str): The API category.
		settings (Optional[Dict[str, Any]]): Configuration settings.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	for target in targets:
		registry = register(
				registry=registry,
				key=target,
				target=target,
				type_=type_,
				api=api,
				method=None,
				settings=settings
		)
	
	return registry


def register_target_methods(
		registry: Dict[str, RegistryItem],
		target: str,
		type_: ITEM_TYPE_TYPEHINT,
		api: str,
		methods: Iterable[str],
		settings: Optional[Dict[str, Any]] = None
) -> Dict[str, RegistryItem]:
	"""
	Registers multiple methods for a single target.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.
		target (str): The target object.
		type_ (ITEM_TYPE): The type of the items.
		api (str): The API category.
		methods (Iterable[str]): A list of methods/properties to register.
		settings (Optional[Dict[str, Any]]): Configuration settings.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	for method in methods:
		registry = register(
				registry=registry,
				key=f"{target}.{method}",
				target=target,
				type_=type_,
				api=api,
				method=method,
				settings=settings
		)
	
	return registry


def register_keys_methods(
		registry: Dict[str, RegistryItem],
		keys: Mapping[str, str],
		type_: ITEM_TYPE_TYPEHINT,
		api: str,
		methods: Iterable[str],
		settings: Optional[Dict[str, Any]] = None
) -> Dict[str, RegistryItem]:
	"""
	Registers methods for multiple targets defined by a mapping of keys to targets.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.
		keys (Mapping[str, str]): Map where key is the registry key prefix and value is the target object.
		type_ (ITEM_TYPE): The type of the items.
		api (str): The API category.
		methods (Iterable[str]): A list of methods to register.
		settings (Optional[Dict[str, Any]]): Configuration settings.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	for key, target in keys.items():
		for method in methods:
			registry = register(
					registry=registry,
					key=f"{key}.{method}",
					target=target,
					type_=type_,
					api=api,
					method=method,
					settings=settings
			)
	
	return registry


def register_key_methods(
		registry: Dict[str, RegistryItem],
		key: str,
		target: str,
		type_: ITEM_TYPE_TYPEHINT,
		api: str,
		methods: Iterable[str],
		settings: Optional[Dict[str, Any]] = None
) -> Dict[str, RegistryItem]:
	"""
	Registers multiple methods for a single target using a custom key prefix.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.
		key (str): The prefix to use for the registry keys.
		target (str): The target object.
		type_ (ITEM_TYPE): The type of the items.
		api (str): The API category.
		methods (Iterable[str]): A list of methods to register.
		settings (Optional[Dict[str, Any]]): Configuration settings.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	for method in methods:
		registry = register(
				registry=registry,
				key=f"{key}.{method}",
				target=target,
				type_=type_,
				api=api,
				method=method,
				settings=settings
		)
	
	return registry
