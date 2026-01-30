from copy import deepcopy
from osn_selenium._base_models import DictModel
from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.flags._functions import argument_to_flag
from osn_selenium.exceptions.logic import (
	AbstractImplementationError
)
from osn_selenium.flags._typehints import (
	ANY_WEBDRIVER_OPTION_TYPEHINT
)
from osn_selenium.exceptions.flags import (
	FlagNotDefinedError,
	FlagTypeNotDefinedError
)
from osn_selenium.flags.models.values import (
	ArgumentValue,
	AttributeValue,
	ExperimentalOptionValue
)
from osn_selenium.flags._validators import (
	bool_adding_validation_function,
	optional_bool_adding_validation_function
)
from osn_selenium.flags.models.base import (
	BrowserArguments,
	BrowserAttributes,
	BrowserExperimentalOptions,
	BrowserFlags,
	FlagDefinition,
	FlagNotDefined,
	FlagType,
	FlagTypeNotDefined
)


__all__ = ["BrowserFlagsManager"]


class BrowserFlagsManager:
	"""
	Manages browser flags, including arguments, experimental options, and attributes for a generic WebDriver.

	This class provides a structured way to define, set, and build browser options
	for various Selenium WebDriver instances.
	"""
	
	def __init__(
			self,
			flags_types: Optional[Dict[str, FlagType]] = None,
			flags_definitions: Optional[Dict[str, FlagDefinition]] = None
	):
		"""
		Initializes the BrowserFlagsManager.

		Args:
			flags_types (Optional[Dict[str, FlagType]]): Custom flag types and their corresponding functions.
			flags_definitions (Optional[Dict[str, FlagDefinition]]): Custom flag definitions to add or override.
		"""
		
		inner_flags_types = {
			"argument": FlagType(
					set_flag_function=self.set_argument,
					remove_flag_function=self.remove_argument,
					set_flags_function=self.set_arguments,
					update_flags_function=self.update_arguments,
					clear_flags_function=self.clear_arguments,
					build_options_function=self._build_options_arguments,
					build_start_args_function=self._build_start_args_arguments
			),
			"experimental_option": FlagType(
					set_flag_function=self.set_experimental_option,
					remove_flag_function=self.remove_experimental_option,
					set_flags_function=self.set_experimental_options,
					update_flags_function=self.update_experimental_options,
					clear_flags_function=self.clear_experimental_options,
					build_options_function=self._build_options_experimental_options,
					build_start_args_function=lambda: [],
			),
			"attribute": FlagType(
					set_flag_function=self.set_attribute,
					remove_flag_function=self.remove_attribute,
					set_flags_function=self.set_attributes,
					update_flags_function=self.update_attributes,
					clear_flags_function=self.clear_attributes,
					build_options_function=self._build_options_attributes,
					build_start_args_function=lambda: [],
			),
		}
		
		if flags_types is not None:
			inner_flags_types.update(flags_types)
		
		inner_flags_definitions = {
			"se_downloads_enabled": FlagDefinition(
					name="se_downloads_enabled",
					command="se:downloadsEnabled",
					type="argument",
					mode="webdriver_option",
					adding_validation_function=bool_adding_validation_function
			),
			"enable_bidi": FlagDefinition(
					name="enable_bidi",
					command="enable_bidi",
					type="attribute",
					mode="webdriver_option",
					adding_validation_function=optional_bool_adding_validation_function
			),
		}
		
		if flags_definitions is not None:
			inner_flags_definitions.update(flags_definitions)
		
		self._flags_types = inner_flags_types
		self._flags_definitions = inner_flags_definitions
		
		self._flags_definitions_by_types: Dict[str, Dict[str, FlagDefinition]] = {
			option_type: dict(
					filter(lambda di: di[1].type == option_type, self._flags_definitions.items())
			)
			for option_type in self._flags_types.keys()
		}
		
		self._arguments: Dict[str, ArgumentValue] = {}
		self._experimental_options: Dict[str, ExperimentalOptionValue] = {}
		self._attributes: Dict[str, AttributeValue] = {}
	
	def _build_options_attributes(self, options: ANY_WEBDRIVER_OPTION_TYPEHINT) -> ANY_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Applies configured attributes to the WebDriver options object.

		Only attributes with `mode` set to 'webdriver_option' or 'both' are applied.

		Args:
			options (any_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			any_webdriver_option_type: The modified WebDriver options object.
		"""
		
		for name, value in self._attributes.items():
			if self._flags_definitions_by_types["attribute"][name].mode in ["webdriver_option", "both"]:
				setattr(options, value.attribute_name, value.value)
		
		return options
	
	def clear_attributes(self):
		"""Clears all configured browser attributes."""
		
		self._attributes = {}
	
	def remove_attribute(self, attribute_name: str):
		"""
		Removes a browser attribute by its attribute name.

		Browser attributes are properties of the WebDriver options object that
		control certain aspects of the browser session. This method removes a previously set attribute.

		Args:
			attribute_name (str): Attribute name of the attribute to remove.
		"""
		
		self._attributes.pop(attribute_name, None)
	
	def set_attribute(self, attribute: FlagDefinition, value: DictModel):
		"""
		Sets a browser attribute. If the attribute already exists, it is overwritten.

		Args:
			attribute (FlagDefinition): The definition of the attribute to set.
			value (DictModel): The value to assign to the attribute.
		"""
		
		attribute_name = attribute.name
		attribute_command = attribute.command
		adding_validation_function = attribute.adding_validation_function
		
		self.remove_attribute(attribute_name)
		
		if adding_validation_function(value):
			self._attributes[attribute_name] = AttributeValue(attribute_name=attribute_command, value=value)
	
	def update_attributes(self, attributes: BrowserAttributes):
		"""
		Updates browser attributes from a dictionary without clearing existing ones.

		Args:
			attributes (BrowserAttributes): A dictionary of attributes to set or update.

		Raises:
			FlagNotDefinedError: If an unknown attribute key is provided.
		"""
		
		for key, value in attributes.model_dump(exclude_none=True).items():
			flag_definition = self._flags_definitions_by_types["attribute"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise FlagNotDefinedError(flag_name=key, flag_type="attributes")
		
			self.set_attribute(flag_definition, getattr(attributes, key))
	
	def set_attributes(self, attributes: BrowserAttributes):
		"""
		Clears existing and sets new browser attributes from a dictionary.

		Args:
			attributes (BrowserAttributes): A dictionary of attributes to set.
		"""
		
		self.clear_attributes()
		self.update_attributes(attributes)
	
	def _build_options_experimental_options(self, options: ANY_WEBDRIVER_OPTION_TYPEHINT) -> ANY_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Adds configured experimental options to the WebDriver options object.

		Only options with `mode` set to 'webdriver_option' or 'both' are added.

		Args:
			options (any_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			any_webdriver_option_type: The modified WebDriver options object.
		"""
		
		for name, value in self._experimental_options.items():
			if self._flags_definitions_by_types["experimental_option"][name].mode in ["webdriver_option", "both"]:
				options.add_experimental_option(value.option_name, value.value)
		
		return options
	
	def clear_experimental_options(self):
		"""Clears all configured experimental options."""
		
		self._experimental_options = {}
	
	def remove_experimental_option(self, experimental_option_name: str):
		"""
		Removes an experimental browser option by its attribute name.

		Experimental options are specific features or behaviors that are not
		part of the standard WebDriver API and may be browser-specific or unstable.
		This method allows for removing such options that were previously set.

		Args:
			experimental_option_name (str): Attribute name of the experimental option to remove.
		"""
		
		self._experimental_options.pop(experimental_option_name, None)
	
	def set_experimental_option(self, experimental_option: FlagDefinition, value: DictModel):
		"""
		Sets an experimental browser option. If the option already exists, it is overwritten.

		Args:
			experimental_option (FlagDefinition): The definition of the experimental option to set.
			value (DictModel): The value to assign to the option.
		"""
		
		experimental_option_name = experimental_option.name
		experimental_option_command = experimental_option.command
		adding_validation_function = experimental_option.adding_validation_function
		
		self.remove_experimental_option(experimental_option_name)
		
		if adding_validation_function(value):
			self._experimental_options[experimental_option_name] = ExperimentalOptionValue(option_name=experimental_option_command, value=value)
	
	def update_experimental_options(self, experimental_options: BrowserExperimentalOptions):
		"""
		Updates experimental options from a dictionary without clearing existing ones.

		Args:
			experimental_options (BrowserExperimentalOptions): A dictionary of experimental options to set or update.

		Raises:
			FlagNotDefinedError: If an unknown experimental option key is provided.
		"""
		
		for key, value in experimental_options.model_dump(exclude_none=True).items():
			flag_definition = self._flags_definitions_by_types["experimental_option"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise FlagNotDefinedError(flag_name=key, flag_type="experimental options")
		
			self.set_experimental_option(flag_definition, getattr(experimental_options, key))
	
	def set_experimental_options(self, experimental_options: BrowserExperimentalOptions):
		"""
		Clears existing and sets new experimental options from a dictionary.

		Args:
			experimental_options (BrowserExperimentalOptions): A dictionary of experimental options to set.
		"""
		
		self.clear_experimental_options()
		self.update_experimental_options(experimental_options)
	
	def _build_start_args_arguments(self) -> List[str]:
		"""
		Builds a List of command-line arguments intended for browser startup.

		Only arguments with `mode` set to 'startup_argument' or 'both' are included.

		Returns:
			List[str]: A List of formatted command-line argument strings.
		"""
		
		return [
			argument_to_flag(value)
			for name, value in self._arguments.items()
			if self._flags_definitions_by_types["argument"][name].mode in ["startup_argument", "both"]
		]
	
	def _build_options_arguments(self, options: ANY_WEBDRIVER_OPTION_TYPEHINT) -> ANY_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Adds configured command-line arguments to the WebDriver options object.

		Only arguments with `mode` set to 'webdriver_option' or 'both' are added.

		Args:
			options (any_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			any_webdriver_option_type: The modified WebDriver options object.
		"""
		
		for name, value in self._arguments.items():
			if self._flags_definitions_by_types["argument"][name].mode in ["webdriver_option", "both"]:
				options.add_argument(argument_to_flag(value))
		
		return options
	
	def clear_arguments(self):
		"""Clears all configured browser arguments."""
		
		self._arguments = {}
	
	def remove_argument(self, argument_name: str):
		"""
		Removes a browser argument by its attribute name.

		Browser arguments are command-line flags that can modify the browser's behavior
		at startup. This method removes an argument that was previously added to the browser options.

		Args:
			argument_name (str): Attribute name of the argument to remove.
		"""
		
		self._arguments.pop(argument_name, None)
	
	def set_argument(self, argument: FlagDefinition, value: Any):
		"""
		Sets a command-line argument. If the argument already exists, it is overwritten.

		Args:
			argument (FlagDefinition): The definition of the argument to set.
			value (Any): The value for the argument. This may be a boolean for a simple flag or a string/number for a valued flag.
		"""
		
		argument_name = argument.name
		argument_command = argument.command
		adding_validation_function = argument.adding_validation_function
		
		self.remove_argument(argument_name)
		
		if adding_validation_function(value):
			self._arguments[argument_name] = ArgumentValue(command_line=argument_command, value=value)
	
	def update_arguments(self, arguments: BrowserArguments):
		"""
		Updates command-line arguments from a dictionary without clearing existing ones.

		Args:
			arguments (BrowserArguments): A dictionary of arguments to set or update.

		Raises:
			FlagNotDefinedError: If an unknown argument key is provided.
		"""
		
		for key, value in arguments.model_dump(exclude_none=True).items():
			flag_definition = self._flags_definitions_by_types["argument"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise FlagNotDefinedError(flag_name=key, flag_type="arguments")
		
			self.set_argument(flag_definition, getattr(arguments, key))
	
	def set_arguments(self, arguments: BrowserArguments):
		"""
		Clears existing and sets new command-line arguments from a dictionary.

		Args:
			arguments (BrowserArguments): A dictionary of arguments to set.
		"""
		
		self.clear_arguments()
		self.update_arguments(arguments)
	
	@property
	def arguments(self) -> Dict[str, ArgumentValue]:
		return deepcopy(self._arguments)
	
	@property
	def attributes(self) -> Dict[str, AttributeValue]:
		return deepcopy(self._attributes)
	
	def clear_flags(self):
		"""Clears all configured flags of all types (arguments, options, attributes)."""
		
		for type_name, type_functions in self._flags_types.items():
			type_functions.clear_flags_function()
	
	@property
	def experimental_options(self) -> Dict[str, ExperimentalOptionValue]:
		return deepcopy(self._experimental_options)
	
	@property
	def flags_definitions(self) -> Dict[str, FlagDefinition]:
		return deepcopy(self._flags_definitions)
	
	@property
	def flags_definitions_by_types(self) -> Dict[str, Dict[str, FlagDefinition]]:
		return deepcopy(self._flags_definitions_by_types)
	
	@property
	def flags_types(self) -> Dict[str, FlagType]:
		return deepcopy(self._flags_types)
	
	def _renew_webdriver_options(self) -> ANY_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Abstract method to renew WebDriver options. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide
		browser-specific WebDriver options instances (e.g., ChromeOptions, FirefoxOptions).

		Returns:
			any_webdriver_option_type: A new instance of WebDriver options (e.g., ChromeOptions, FirefoxOptions).

		Raises:
			AbstractImplementationError: If the method is not implemented in a subclass.
		"""
		
		raise AbstractImplementationError(
				method_name="_renew_webdriver_options",
				class_name=self.__class__.__name__
		)
	
	@property
	def options(self) -> ANY_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Builds and returns a WebDriver options object with all configured flags applied.

		Returns:
			any_webdriver_option_type: A configured WebDriver options object.
		"""
		
		options = self._renew_webdriver_options()
		
		for type_name, type_functions in self._flags_types.items():
			options = type_functions.build_options_function(options)
		
		return options
	
	def remove_option(self, option: FlagDefinition):
		"""
		Removes a browser option by its configuration object.

		This method removes a browser option, whether it's a normal argument,
		an experimental option, or an attribute, based on the provided `WebdriverOption` configuration.
		It determines the option type and calls the appropriate removal method.

		Args:
			option (WebdriverOption): The configuration object defining the option to be removed.

		Raises:
			FlagTypeNotDefinedError: If the option type is not recognized.
		"""
		
		for type_name, type_functions in self._flags_types.items():
			if option.type == type_name:
				type_functions.remove_flag_function(option.name)
		
		raise FlagTypeNotDefinedError(flag_type=option.type)
	
	def set_flags(self, flags: BrowserFlags):
		"""
		Clears all existing flags and sets new ones from a comprehensive dictionary.

		This method iterates through the provided flag types (e.g., 'arguments', 'experimental_options')
		and calls the corresponding `set_*` function for each type, effectively replacing all
		previously configured flags for that type.

		Args:
			flags (BrowserFlags): A dictionary where keys are flag types
				and values are dictionaries of flags to set for that type.

		Raises:
			FlagTypeNotDefinedError: If an unknown flag type is provided in the `flags` dictionary.
		"""
		
		for type_name, type_flags in flags.model_dump(exclude_none=True).items():
			flags_type_definition = self._flags_types.get(type_name, FlagTypeNotDefined())
		
			if isinstance(flags_type_definition, FlagTypeNotDefined):
				raise FlagTypeNotDefinedError(flag_type=type_name)
		
			flags_type_definition.set_flags_function(getattr(flags, type_name))
	
	def set_option(self, option: FlagDefinition, value: Any):
		"""
		Sets a browser option based on its configuration object.

		This method configures a browser option, handling normal arguments,
		experimental options, and attributes as defined in the provided `FlagDefinition`.
		It uses the option's type to determine the appropriate method for setting the option with the given value.

		Args:
			option (FlagDefinition): A dictionary-like object containing the configuration for the option to be set.
			value (Any): The value to be set for the option. The type and acceptable values depend on the specific browser option being configured.

		Raises:
			FlagTypeNotDefinedError: If the option type is not recognized.
		"""
		
		for type_name, type_functions in self._flags_types.items():
			if option.type == type_name:
				type_functions.set_flag_function(option, value)
		
		raise FlagTypeNotDefinedError(flag_type=option.type)
	
	def update_flags(self, flags: BrowserFlags):
		"""
		Updates all flags from a comprehensive dictionary without clearing existing ones.

		This method iterates through the provided flag types (e.g., 'arguments', 'experimental_options')
		and calls the corresponding `update_*` function for each type, adding or overwriting
		flags without affecting other existing flags.

		Args:
			flags (BrowserFlags): A dictionary where keys are flag types
				and values are dictionaries of flags to update for that type.

		Raises:
			FlagTypeNotDefinedError: If an unknown flag type is provided in the `flags` dictionary.
		"""
		
		for type_name, type_flags in flags.model_dump(exclude_none=True).items():
			flags_type_definition = self._flags_types.get(type_name, FlagTypeNotDefined())
		
			if isinstance(flags_type_definition, FlagTypeNotDefined):
				raise FlagTypeNotDefinedError(flag_type=type_name)
		
			flags_type_definition.update_flags_function(getattr(flags, type_name))
