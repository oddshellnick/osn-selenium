from typing import Dict, Optional
from osn_selenium._typehints import PATH_TYPEHINT
from selenium.webdriver.chrome.options import Options
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_selenium.flags.models.blink import BlinkFeatures
from osn_selenium.flags.models.base import (
	FlagDefinition,
	FlagType
)
from osn_selenium.flags.models.edge import (
	EdgeArguments,
	EdgeAttributes,
	EdgeExperimentalOptions,
	EdgeFlags
)


__all__ = ["EdgeFlagsManager"]


class EdgeFlagsManager(BlinkFlagsManager):
	"""
	Manages Edge Browser-specific options for Selenium WebDriver.

	This class extends BrowserOptionsManager to provide specific configurations
	for Edge Browser options, such as experimental options and arguments.

	Attributes:
	"""
	
	def __init__(
			self,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			start_page_url: Optional[str] = None,
			flags_types: Optional[Dict[str, FlagType]] = None,
			flags_definitions: Optional[Dict[str, FlagDefinition]] = None
	):
		"""
		Initializes EdgeOptionsManager.

		Sets up the Edge Browser options manager with specific option configurations for
		debugging port, user agent, proxy, and BiDi protocol.
		"""
		
		yandex_flags_types = {}
		
		if flags_types is not None:
			yandex_flags_types.update(flags_types)
		
		yandex_flags_definitions = {}
		
		if flags_definitions is not None:
			yandex_flags_definitions.update(flags_definitions)
		
		super().__init__(
				browser_exe=browser_exe,
				start_page_url=start_page_url,
				flags_types=yandex_flags_types,
				flags_definitions=yandex_flags_definitions,
		)
	
	def _build_options_arguments(self, options: Options) -> Options:
		"""
		Adds configured command-line arguments to the WebDriver options.

		Args:
			options (Options): The WebDriver options object.

		Returns:
			Options: The modified WebDriver options object.
		"""
		
		return super()._build_options_arguments(options)
	
	def _build_options_attributes(self, options: Options) -> Options:
		"""
		Applies configured attributes to the WebDriver options.

		Args:
			options (Options): The WebDriver options object.

		Returns:
			Options: The modified WebDriver options object.
		"""
		
		return super()._build_options_attributes(options)
	
	def _build_options_blink_features(self, options: Options) -> Options:
		"""
		Adds configured Edge features (`--enable-blink-features` and `--disable-blink-features`) to the WebDriver options.

		Args:
			options (Options): The WebDriver options object to modify.

		Returns:
			Options: The modified WebDriver options object.
		"""
		
		return super()._build_options_blink_features(options)
	
	def _build_options_experimental_options(self, options: Options) -> Options:
		"""
		Adds experimental options to the WebDriver options.

		Args:
			options (Options): The WebDriver options object.

		Returns:
			Options: The modified WebDriver options object.
		"""
		
		return super()._build_options_experimental_options(options)
	
	def _renew_webdriver_options(self) -> Options:
		"""
		Creates and returns a new Options object.

		Returns a fresh instance of `webdriver.EdgeOptions`, as Edge Browser is based on Chromium,
		allowing for a clean state of browser options to be configured.

		Returns:
			Options: A new Selenium Edge Browser options object, based on EdgeOptions.
		"""
		
		return Options()
	
	def set_arguments(self, arguments: EdgeArguments):
		"""
		Clears existing and sets new command-line arguments from a dictionary.

		Args:
			arguments (EdgeArguments): A dictionary of arguments to set.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		super().set_arguments(arguments)
	
	def set_attributes(self, attributes: EdgeAttributes):
		"""
		Clears existing and sets new browser attributes from a dictionary.

		Args:
			attributes (EdgeAttributes): A dictionary of attributes to set.

		Raises:
			ValueError: If an unknown attribute key is provided.
		"""
		
		super().set_attributes(attributes)
	
	def set_blink_features(self, blink_features: BlinkFeatures):
		"""
		Clears existing and sets new Edge features from a dictionary.

		Args:
			blink_features (BlinkFeatures): A dictionary of Edge features to set.

		Raises:
			ValueError: If an unknown Edge feature key is provided.
		"""
		
		super().set_blink_features(blink_features)
	
	def set_experimental_options(self, experimental_options: EdgeExperimentalOptions):
		"""
		Clears existing and sets new experimental options from a dictionary.

		Args:
			experimental_options (EdgeExperimentalOptions): A dictionary of experimental options to set.

		Raises:
			ValueError: If an unknown experimental option key is provided.
		"""
		
		super().set_experimental_options(experimental_options)
	
	def set_flags(self, flags: EdgeFlags):
		"""
		Clears all existing flags and sets new ones, including Edge features.

		This method delegates to the parent `set_flags` method, allowing it to handle
		all flag types defined in this manager, including 'arguments', 'experimental_options',
		'attributes', and 'blink_features'.

		Args:
			flags (EdgeFlags): A dictionary where keys are flag types
				and values are dictionaries of flags to set for that type.
		"""
		
		super().set_flags(flags)
	
	def update_arguments(self, arguments: EdgeArguments):
		"""
		Updates command-line arguments from a dictionary without clearing existing ones.

		Args:
			arguments (EdgeArguments): A dictionary of arguments to set or update.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		super().update_arguments(arguments)
	
	def update_attributes(self, attributes: EdgeAttributes):
		"""
		Updates browser attributes from a dictionary without clearing existing ones.

		Args:
			attributes (EdgeAttributes): A dictionary of attributes to set or update.

		Raises:
			ValueError: If an unknown attribute key is provided.
		"""
		
		super().update_attributes(attributes)
	
	def update_blink_features(self, blink_features: BlinkFeatures):
		"""
		Updates Edge features from a dictionary without clearing existing ones.

		Args:
			blink_features (BlinkFeatures): A dictionary of Edge features to set or update.

		Raises:
			ValueError: If an unknown Edge feature key is provided.
		"""
		
		super().update_blink_features(blink_features)
	
	def update_experimental_options(self, experimental_options: EdgeExperimentalOptions):
		"""
		Updates experimental options from a dictionary without clearing existing ones.

		Args:
			experimental_options (EdgeExperimentalOptions): A dictionary of experimental options to set or update.

		Raises:
			ValueError: If an unknown experimental option key is provided.
		"""
		
		super().update_experimental_options(experimental_options)
	
	def update_flags(self, flags: EdgeFlags):
		"""
		Updates all flags, including Edge features, without clearing existing ones.

		This method delegates to the parent `update_flags` method, allowing it to handle
		all flag types defined in this manager, including 'arguments', 'experimental_options',
		'attributes', and 'blink_features'.

		Args:
			flags (EdgeFlags): A dictionary where keys are flag types
				and values are dictionaries of flags to update for that type.
		"""
		
		super().update_flags(flags)
