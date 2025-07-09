from typing import (
	Any,
	Optional,
	TypedDict,
	Union
)
from osn_selenium.webdrivers.types import (
	FlagDefinition,
	FlagNotDefined,
	FlagType,
	_any_webdriver_option_type
)
from osn_selenium.webdrivers._functions import (
	bool_adding_validation_function,
	optional_bool_adding_validation_function
)


class ArgumentValue(TypedDict):
	"""
	Typed dictionary representing a single command-line argument and its value.

	Attributes:
		command_line (str): The command-line string for the argument.
		value (Any): The value associated with the argument.
	"""
	
	command_line: str
	value: Any


def _argument_to_flag(argument: ArgumentValue) -> str:
	"""
	Formats a command-line argument from an ArgumentValue dictionary.

	If the command string contains '{value}', it will be replaced by the argument's value.
	Otherwise, the command string is returned as is.

	Args:
		argument (ArgumentValue): A dictionary containing the command-line string and its value.

	Returns:
		str: The formatted command-line argument string.
	"""
	
	argument_command = argument["command_line"]
	argument_value = argument["value"]
	
	if "{value}" in argument_command:
		return argument_command.format(value=argument_value)
	else:
		return argument_command


class ExperimentalOptionValue(TypedDict):
	"""
	Typed dictionary representing a single experimental option and its value.

	Attributes:
		option_name (str): The name of the experimental option.
		value (Any): The value of the experimental option.
	"""
	
	option_name: str
	value: Any


class AttributeValue(TypedDict):
	"""
	Typed dictionary representing a single WebDriver attribute and its value.

	Attributes:
		attribute_name (str): The name of the attribute.
		value (Any): The value of the attribute.
	"""
	
	attribute_name: str
	value: Any


class FlagTypeNotDefined:
	"""A sentinel class to indicate that a flag type definition was not found."""
	
	pass


class BrowserExperimentalOptions(TypedDict, total=False):
	"""
	Typed dictionary for browser-agnostic experimental options.
	"""
	
	pass


class BrowserAttributes(TypedDict, total=False):
	"""
	Typed dictionary for browser-agnostic WebDriver attributes.

	Attributes:
		enable_bidi (Optional[bool]): Enables/disables BiDi (Bidirectional) protocol mapper.
	"""
	
	enable_bidi: Optional[bool]


class BrowserArguments(TypedDict, total=False):
	"""
	Typed dictionary for browser-agnostic command-line arguments.

	Attributes:
		se_downloads_enabled (bool): Enables/disables Selenium downloads.
	"""
	
	se_downloads_enabled: bool


class BrowserFlags(TypedDict, total=False):
	"""
	Typed dictionary representing a collection of all flag types.

	Attributes:
		argument (BrowserArguments): Command-line arguments for the browser.
		experimental_option (BrowserExperimentalOptions): Experimental options for WebDriver.
		attribute (BrowserAttributes): WebDriver attributes.
	"""
	
	argument: BrowserArguments
	experimental_option: BrowserExperimentalOptions
	attribute: BrowserAttributes


class BrowserFlagsManager:
	"""
	Manages browser flags, including arguments, experimental options, and attributes for a generic WebDriver.

	This class provides a structured way to define, set, and build browser options
	for various Selenium WebDriver instances.

	Attributes:
		_flags_types (dict[str, FlagType]): A dictionary mapping flag types to their handler functions.
		_flags_definitions (dict[str, FlagDefinition]): A dictionary of all available flag definitions.
		_flags_definitions_by_types (dict[str, dict[str, FlagDefinition]]): Flags definitions grouped by type.
		_arguments (dict[str, ArgumentValue]): Stores the configured command-line arguments.
		_experimental_options (dict[str, ExperimentalOptionValue]): Stores the configured experimental options.
		_attributes (dict[str, AttributeValue]): Stores the configured WebDriver attributes.
	"""
	
	def __init__(
			self,
			flags_types: Optional[dict[str, FlagType]] = None,
			flags_definitions: Optional[dict[str, FlagDefinition]] = None
	):
		"""
		Initializes the BrowserFlagsManager.

		Args:
			flags_types (Optional[dict[str, FlagType]]): Custom flag types and their corresponding functions.
			flags_definitions (Optional[dict[str, FlagDefinition]]): Custom flag definitions to add or override.
		"""
		
		inner_flags_types = {
			"argument": FlagType(
					set_flag_function=self.set_argument,
					remove_flag_function=self.remove_argument,
					set_flags_function=self.set_arguments,
					update_flags_function=self.update_arguments,
					clear_flags_function=self.clear_arguments,
					build_options_function=self.build_options_arguments,
					build_start_args_function=self.build_start_args_arguments
			),
			"experimental_option": FlagType(
					set_flag_function=self.set_experimental_option,
					remove_flag_function=self.remove_experimental_option,
					set_flags_function=self.set_experimental_options,
					update_flags_function=self.update_experimental_options,
					clear_flags_function=self.clear_experimental_options,
					build_options_function=self.build_options_experimental_options,
					build_start_args_function=lambda: []
			),
			"attribute": FlagType(
					set_flag_function=self.set_attribute,
					remove_flag_function=self.remove_attribute,
					set_flags_function=self.set_attributes,
					update_flags_function=self.update_attributes,
					clear_flags_function=self.clear_attributes,
					build_options_function=self.build_options_attributes,
					build_start_args_function=lambda: []
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
		
		self._flags_definitions_by_types: dict[str, dict[str, FlagDefinition]] = {
			option_type: dict(
					filter(lambda di: di[1]["type"] == option_type, self._flags_definitions.items())
			)
			for option_type in self._flags_types.keys()
		}
		
		self._arguments: dict[str, ArgumentValue] = {}
		self._experimental_options: dict[str, ExperimentalOptionValue] = {}
		self._attributes: dict[str, AttributeValue] = {}
	
	def build_options_attributes(self, options: _any_webdriver_option_type) -> _any_webdriver_option_type:
		"""
		Applies configured attributes to the WebDriver options object.

		Only attributes with `mode` set to 'webdriver_option' or 'both' are applied.

		Args:
			options (_any_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			_any_webdriver_option_type: The modified WebDriver options object.
		"""
		
		for name, value in self._attributes.items():
			if self._flags_definitions_by_types["attribute"][name]["mode"] in ["webdriver_option", "both"]:
				setattr(options, value["attribute_name"], value["value"])
		
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
	
	def set_attribute(self, attribute: FlagDefinition, value: Any):
		"""
		Sets a browser attribute. If the attribute already exists, it is overwritten.

		Args:
			attribute (FlagDefinition): The definition of the attribute to set.
			value (Any): The value to assign to the attribute.
		"""
		
		attribute_name = attribute["name"]
		attribute_command = attribute["command"]
		adding_validation_function = attribute["adding_validation_function"]
		
		self.remove_attribute(attribute_name)
		
		if adding_validation_function(value):
			self._attributes[attribute_name] = AttributeValue(attribute_name=attribute_command, value=value)
	
	def update_attributes(self, attributes: Union[BrowserAttributes, dict[str, Any]]):
		"""
		Updates browser attributes from a dictionary without clearing existing ones.

		Args:
			attributes (Union[BrowserAttributes, dict[str, Any]]): A dictionary of attributes to set or update.

		Raises:
			ValueError: If an unknown attribute key is provided.
		"""
		
		for key, value in attributes.items():
			flag_definition = self._flags_definitions_by_types["attribute"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise ValueError(f"Unknown attribute: {key}.")
		
			self.set_attribute(flag_definition, value)
	
	def set_attributes(self, attributes: Union[BrowserAttributes, dict[str, Any]]):
		"""
		Clears existing and sets new browser attributes from a dictionary.

		Args:
			attributes (Union[BrowserAttributes, dict[str, Any]]): A dictionary of attributes to set.

		Raises:
			ValueError: If an unknown attribute key is provided.
		"""
		
		self.clear_attributes()
		self.update_attributes(attributes)
	
	def build_options_experimental_options(self, options: _any_webdriver_option_type) -> _any_webdriver_option_type:
		"""
		Adds configured experimental options to the WebDriver options object.

		Only options with `mode` set to 'webdriver_option' or 'both' are added.

		Args:
			options (_any_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			_any_webdriver_option_type: The modified WebDriver options object.
		"""
		
		for name, value in self._experimental_options.items():
			if self._flags_definitions_by_types["experimental_option"][name]["mode"] in ["webdriver_option", "both"]:
				options.add_experimental_option(value["option_name"], value["value"])
		
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
	
	def set_experimental_option(self, experimental_option: FlagDefinition, value: Any):
		"""
		Sets an experimental browser option. If the option already exists, it is overwritten.

		Args:
			experimental_option (FlagDefinition): The definition of the experimental option to set.
			value (Any): The value to assign to the option.
		"""
		
		experimental_option_name = experimental_option["name"]
		experimental_option_command = experimental_option["command"]
		adding_validation_function = experimental_option["adding_validation_function"]
		
		self.remove_experimental_option(experimental_option_name)
		
		if adding_validation_function(value):
			self._experimental_options[experimental_option_name] = ExperimentalOptionValue(option_name=experimental_option_command, value=value)
	
	def update_experimental_options(
			self,
			experimental_options: Union[BrowserExperimentalOptions, dict[str, Any]]
	):
		"""
		Updates experimental options from a dictionary without clearing existing ones.

		Args:
			experimental_options (Union[BrowserExperimentalOptions, dict[str, Any]]): A dictionary of experimental options to set or update.

		Raises:
			ValueError: If an unknown experimental option key is provided.
		"""
		
		for key, value in experimental_options.items():
			flag_definition = self._flags_definitions_by_types["experimental_option"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise ValueError(f"Unknown experimental option: {key}.")
		
			self.set_experimental_option(flag_definition, value)
	
	def set_experimental_options(
			self,
			experimental_options: Union[BrowserExperimentalOptions, dict[str, Any]]
	):
		"""
		Clears existing and sets new experimental options from a dictionary.

		Args:
			experimental_options (Union[BrowserExperimentalOptions, dict[str, Any]]): A dictionary of experimental options to set.

		Raises:
			ValueError: If an unknown experimental option key is provided.
		"""
		
		self.clear_experimental_options()
		self.update_experimental_options(experimental_options)
	
	def build_start_args_arguments(self) -> list[str]:
		"""
		Builds a list of command-line arguments intended for browser startup.

		Only arguments with `mode` set to 'startup_argument' or 'both' are included.

		Returns:
			list[str]: A list of formatted command-line argument strings.
		"""
		
		return [
			_argument_to_flag(value)
			for name, value in self._arguments.items()
			if self._flags_definitions_by_types["argument"][name]["mode"] in ["startup_argument", "both"]
		]
	
	def build_options_arguments(self, options: _any_webdriver_option_type) -> _any_webdriver_option_type:
		"""
		Adds configured command-line arguments to the WebDriver options object.

		Only arguments with `mode` set to 'webdriver_option' or 'both' are added.

		Args:
			options (_any_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			_any_webdriver_option_type: The modified WebDriver options object.
		"""
		
		for name, value in self._arguments.items():
			if self._flags_definitions_by_types["argument"][name]["mode"] in ["webdriver_option", "both"]:
				options.add_argument(_argument_to_flag(value))
		
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
		
		argument_name = argument["name"]
		argument_command = argument["command"]
		adding_validation_function = argument["adding_validation_function"]
		
		self.remove_argument(argument_name)
		
		if adding_validation_function(value):
			self._arguments[argument_name] = ArgumentValue(command_line=argument_command, value=value)
	
	def update_arguments(self, arguments: Union[BrowserArguments, dict[str, Any]]):
		"""
		Updates command-line arguments from a dictionary without clearing existing ones.

		Args:
			arguments (Union[BrowserArguments, dict[str, Any]]): A dictionary of arguments to set or update.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		for key, value in arguments.items():
			flag_definition = self._flags_definitions_by_types["argument"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise ValueError(f"Unknown argument: {key}.")
		
			self.set_argument(flag_definition, value)
	
	def set_arguments(self, arguments: Union[BrowserArguments, dict[str, Any]]):
		"""
		Clears existing and sets new command-line arguments from a dictionary.

		Args:
			arguments (Union[BrowserArguments, dict[str, Any]]): A dictionary of arguments to set.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		self.clear_arguments()
		self.update_arguments(arguments)
	
	def clear_flags(self):
		"""Clears all configured flags of all types (arguments, options, attributes)."""
		
		for type_name, type_functions in self._flags_types.items():
			type_functions["clear_flags_function"]()
	
	def _renew_webdriver_options(self) -> _any_webdriver_option_type:
		"""
		Abstract method to renew WebDriver options. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide
		browser-specific WebDriver options instances (e.g., ChromeOptions, FirefoxOptions).

		Returns:
			_any_webdriver_option_type: A new instance of WebDriver options (e.g., ChromeOptions, FirefoxOptions).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		raise NotImplementedError("This function must be implemented in child classes.")
	
	@property
	def options(self) -> _any_webdriver_option_type:
		"""
		Builds and returns a WebDriver options object with all configured flags applied.

		Returns:
			_any_webdriver_option_type: A configured WebDriver options object.
		"""
		
		options = self._renew_webdriver_options()
		
		for type_name, type_functions in self._flags_types.items():
			options = type_functions["build_options_function"](options)
		
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
			ValueError: If the option type is not recognized.
		"""
		
		for type_name, type_functions in self._flags_types.items():
			if option["type"] == type_name:
				type_functions["remove_flag_function"](option["name"])
		
		raise ValueError(f"Unknown option type ({option}).")
	
	def set_flags(self, flags: Union[BrowserFlags, dict[str, dict[str, Any]]]):
		"""
		Clears all existing flags and sets new ones from a comprehensive dictionary.

		This method iterates through the provided flag types (e.g., 'arguments', 'experimental_options')
		and calls the corresponding `set_*` function for each type, effectively replacing all
		previously configured flags for that type.

		Args:
			flags (Union[BrowserFlags, dict[str, dict[str, Any]]]): A dictionary where keys are flag types
				and values are dictionaries of flags to set for that type.

		Raises:
			ValueError: If an unknown flag type is provided in the `flags` dictionary.
		"""
		
		for type_name, type_flags in flags.items():
			flags_type_definition = self._flags_types.get(type_name, FlagTypeNotDefined())
		
			if isinstance(flags_type_definition, FlagTypeNotDefined):
				raise ValueError(f"Unknown flag type: {type_name}.")
		
			flags_type_definition["set_flags_function"](type_flags)
	
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
			ValueError: If the option type is not recognized.
		"""
		
		for type_name, type_functions in self._flags_types.items():
			if option["type"] == type_name:
				type_functions["set_flag_function"](option, value)
		
		raise ValueError(
				f"Unknown option type ({option}). Acceptable types are: {', '.join(self._flags_types.keys())}."
		)
	
	def update_flags(self, flags: Union[BrowserFlags, dict[str, dict[str, Any]]]):
		"""
		Updates all flags from a comprehensive dictionary without clearing existing ones.

		This method iterates through the provided flag types (e.g., 'arguments', 'experimental_options')
		and calls the corresponding `update_*` function for each type, adding or overwriting
		flags without affecting other existing flags.

		Args:
			flags (Union[BrowserFlags, dict[str, dict[str, Any]]]): A dictionary where keys are flag types
				and values are dictionaries of flags to update for that type.

		Raises:
			ValueError: If an unknown flag type is provided in the `flags` dictionary.
		"""
		
		for type_name, type_flags in flags.items():
			flags_type_definition = self._flags_types.get(type_name, FlagTypeNotDefined())
		
			if isinstance(flags_type_definition, FlagTypeNotDefined):
				raise ValueError(f"Unknown flag type: {type_name}.")
		
			flags_type_definition["update_flags_function"](type_flags)
