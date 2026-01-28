from pydantic import Field
from typing import (
	Any,
	Callable,
	List,
	Literal,
	Optional
)
from osn_selenium._base_models import (
	DictModel,
	ExtraDictModel
)
from osn_selenium.flags._typehints import (
	ANY_WEBDRIVER_OPTION_TYPEHINT
)


__all__ = [
	"BrowserArguments",
	"BrowserAttributes",
	"BrowserExperimentalOptions",
	"BrowserFlags",
	"FlagDefinition",
	"FlagNotDefined",
	"FlagType",
	"FlagTypeNotDefined"
]


class FlagTypeNotDefined:
	"""
	Sentinel indicating missing flag type definition.
	"""
	
	pass


class FlagDefinition(DictModel):
	"""
	Defines a browser flag with name, command, type, and how it is applied.

	Attributes:
		name (str): Internal name of the flag.
		command (str): Command-line argument or key.
		type (Literal): Category of the flag (e.g., argument, attribute).
		mode (Literal): How the flag is applied (e.g., startup, webdriver).
		adding_validation_function (Callable): Validator function for the value.
	"""
	
	name: str
	command: str
	type: Literal["argument", "experimental_option", "attribute", "blink_feature"]
	mode: Literal["webdriver_option", "startup_argument", "both"]
	adding_validation_function: Callable[[Any], bool]


class FlagType(DictModel):
	"""
	Represents callable interfaces for setting and managing browser flags.

	Attributes:
		set_flag_function (Callable): Function to set a single flag.
		remove_flag_function (Callable): Function to remove a flag.
		set_flags_function (Callable): Function to set multiple flags.
		update_flags_function (Callable): Function to update multiple flags.
		clear_flags_function (Callable): Function to clear all flags.
		build_options_function (Callable): Builds webdriver options.
		build_start_args_function (Callable): Builds command-line arguments.
	"""
	
	set_flag_function: Callable[[FlagDefinition, Any], None]
	remove_flag_function: Callable[[str], None]
	set_flags_function: Callable[[ExtraDictModel], None]
	update_flags_function: Callable[[ExtraDictModel], None]
	clear_flags_function: Callable[..., None]
	build_options_function: Callable[[ANY_WEBDRIVER_OPTION_TYPEHINT], ANY_WEBDRIVER_OPTION_TYPEHINT]
	build_start_args_function: Callable[..., List[str]]


class FlagNotDefined:
	"""
	A sentinel class to indicate that a flag definition was not found.
	"""
	
	pass


class BrowserAttributes(ExtraDictModel):
	"""
	WebDriver attributes for browser.

	Attributes:
		enable_bidi (Optional[bool]): Enable/disable BiDi protocol.
	"""
	
	enable_bidi: Optional[bool] = None


class BrowserExperimentalOptions(ExtraDictModel):
	"""
	WebDriver experimental options for browser.
	"""
	
	pass


class BrowserArguments(ExtraDictModel):
	"""
	WebDriver command-line arguments.

	Attributes:
		se_downloads_enabled (Optional[bool]): Enable Selenium downloads.
	"""
	
	se_downloads_enabled: Optional[bool] = None


class BrowserFlags(DictModel):
	"""
	Combined structure of all browser flags.

	Attributes:
		argument (BrowserArguments): Command-line arguments.
		experimental_option (BrowserExperimentalOptions): Experimental options.
		attribute (BrowserAttributes): WebDriver attributes.
	"""
	
	argument: BrowserArguments = Field(default_factory=BrowserArguments)
	experimental_option: BrowserExperimentalOptions = Field(default_factory=BrowserExperimentalOptions)
	attribute: BrowserAttributes = Field(default_factory=BrowserAttributes)
