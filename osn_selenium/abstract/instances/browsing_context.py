from abc import ABC, abstractmethod
from typing import (
	Callable,
	Mapping,
	Optional,
	Sequence,
	Union
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext,
	BrowsingContextInfo
)


__all__ = ["AbstractBrowsingContext"]


class AbstractBrowsingContext(ABC):
	"""
	Abstract base class for managing browsing contexts.

	Defines the interface for creating, closing, navigating, and interacting
	with browsing contexts (e.g., tabs, windows).
	"""
	
	@abstractmethod
	def activate(self, context: str) -> None:
		"""
		Activates (brings to the front) a browsing context.

		Args:
			context (str): The ID of the browsing context to activate.
		"""
		
		...
	
	@abstractmethod
	def add_event_handler(
			self,
			event: str,
			callback: Callable,
			contexts: Optional[Sequence[str]] = None,
	) -> int:
		"""
		Adds an event handler for browsing context events.

		Args:
			event (str): The name of the event to listen for.
			callback (Callable): The function to call when the event occurs.
			contexts (Optional[Sequence[str]]): A list of context IDs to listen on.

		Returns:
			int: The ID of the newly added event handler.
		"""
		
		...
	
	@abstractmethod
	def capture_screenshot(
			self,
			context: str,
			origin: str = 'viewport',
			format: Optional[Mapping] = None,
			clip: Optional[Mapping] = None,
	) -> str:
		"""
		Captures a screenshot of a browsing context.

		Args:
			context (str): The ID of the browsing context to capture.
			origin (str): The origin of the screenshot ('viewport' or 'document').
			format (Optional[Mapping]): Image format options.
			clip (Optional[Mapping]): A clip rectangle to capture a specific area.

		Returns:
			str: A base64-encoded string of the screenshot image data.
		"""
		
		...
	
	@abstractmethod
	def clear_event_handlers(self) -> None:
		"""
		Clears all registered event handlers for browsing contexts.
		"""
		
		...
	
	@abstractmethod
	def close(self, context: str, prompt_unload: bool = False) -> None:
		"""
		Closes a browsing context.

		Args:
			context (str): The ID of the browsing context to close.
			prompt_unload (bool): Whether to handle any beforeunload prompts.
		"""
		
		...
	
	@abstractmethod
	def create(
			self,
			type: str,
			reference_context: Optional[str] = None,
			background: bool = False,
			user_context: Optional[str] = None,
	) -> str:
		"""
		Creates a new browsing context.

		Args:
			type (str): The type of context to create ('tab' or 'window').
			reference_context (Optional[str]): A reference context for positioning.
			background (bool): Whether to create the context in the background.
			user_context (Optional[str]): The user context to create it in.

		Returns:
			str: The ID of the newly created browsing context.
		"""
		
		...
	
	@abstractmethod
	def get_tree(self, max_depth: Optional[int] = None, root: Optional[str] = None) -> Sequence[BrowsingContextInfo]:
		"""
		Retrieves the tree of browsing contexts.

		Args:
			max_depth (Optional[int]): The maximum depth of the tree to retrieve.
			root (Optional[str]): The root context ID to start from.

		Returns:
			Sequence[BrowsingContextInfo]: A sequence of browsing context information objects.
		"""
		
		...
	
	@abstractmethod
	def handle_user_prompt(
			self,
			context: str,
			accept: Optional[bool] = None,
			user_text: Optional[str] = None,
	) -> None:
		"""
		Handles a user prompt (e.g., alert, confirm, prompt).

		Args:
			context (str): The ID of the browsing context with the prompt.
			accept (Optional[bool]): Whether to accept or dismiss the prompt.
			user_text (Optional[str]): Text to enter into a prompt.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyBrowsingContext:
		"""
		Returns the underlying legacy Selenium BrowsingContext instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyBrowsingContext: The legacy Selenium BrowsingContext object.
		"""
		
		...
	
	@abstractmethod
	def locate_nodes(
			self,
			context: str,
			locator: Mapping,
			max_node_count: Optional[int] = None,
			serialization_options: Optional[Mapping] = None,
			start_nodes: Optional[Sequence[Mapping]] = None,
	) -> Sequence[Mapping]:
		"""
		Locates nodes within a browsing context.

		Args:
			context (str): The ID of the browsing context.
			locator (Mapping): The locator strategy and value.
			max_node_count (Optional[int]): The maximum number of nodes to return.
			serialization_options (Optional[Mapping]): Options for serializing the nodes.
			start_nodes (Optional[Sequence[Mapping]]): Nodes to start the search from.

		Returns:
			Sequence[Mapping]: A sequence of found nodes.
		"""
		
		...
	
	@abstractmethod
	def navigate(self, context: str, url: str, wait: Optional[str] = None) -> Mapping:
		"""
		Navigates a browsing context to a new URL.

		Args:
			context (str): The ID of the browsing context.
			url (str): The URL to navigate to.
			wait (Optional[str]): The page load strategy ('none', 'eager', 'interactive', 'complete').

		Returns:
			Mapping: A dictionary with navigation information.
		"""
		
		...
	
	@abstractmethod
	def print(
			self,
			context: str,
			background: bool = False,
			margin: Optional[Mapping] = None,
			orientation: str = 'portrait',
			page: Optional[Mapping] = None,
			page_ranges: Optional[Sequence[Union[int, str]]] = None,
			scale: float = 1.0,
			shrink_to_fit: bool = True,
	) -> str:
		"""
		Prints the page to a PDF.

		Args:
			context (str): The ID of the browsing context.
			background (bool): Whether to print background graphics.
			margin (Optional[Mapping]): Margins for the page.
			orientation (str): Page orientation ('portrait' or 'landscape').
			page (Optional[Mapping]): Page size settings.
			page_ranges (Optional[Sequence[Union[int, str]]]): Page ranges to print.
			scale (float): The scale of the webpage rendering.
			shrink_to_fit (bool): Whether to shrink the content to fit the page size.

		Returns:
			str: A base64-encoded string of the PDF data.
		"""
		
		...
	
	@abstractmethod
	def reload(
			self,
			context: str,
			ignore_cache: Optional[bool] = None,
			wait: Optional[str] = None,
	) -> Mapping:
		"""
		Reloads the current page in a browsing context.

		Args:
			context (str): The ID of the browsing context.
			ignore_cache (Optional[bool]): If True, bypasses the cache.
			wait (Optional[str]): The page load strategy ('none', 'eager', 'interactive', 'complete').

		Returns:
			Mapping: A dictionary with navigation information.
		"""
		
		...
	
	@abstractmethod
	def remove_event_handler(self, event: str, callback_id: int) -> None:
		"""
		Removes an event handler.

		Args:
			event (str): The name of the event.
			callback_id (int): The ID of the handler to remove.
		"""
		
		...
	
	@abstractmethod
	def set_viewport(
			self,
			context: Optional[str] = None,
			viewport: Optional[Mapping] = None,
			device_pixel_ratio: Optional[float] = None,
			user_contexts: Optional[Sequence[str]] = None,
	) -> None:
		"""
		Sets the viewport for a browsing context.

		Args:
			context (Optional[str]): The ID of the browsing context.
			viewport (Optional[Mapping]): A dictionary with 'width' and 'height'.
			device_pixel_ratio (Optional[float]): The device pixel ratio.
			user_contexts (Optional[Sequence[str]]): A sequence of user context IDs to apply this to.
		"""
		
		...
	
	@abstractmethod
	def traverse_history(self, context: str, delta: int) -> Mapping:
		"""
		Traverses the browsing history by a given delta.

		Args:
			context (str): The ID of the browsing context.
			delta (int): The number of steps to go forward (positive) or backward (negative).

		Returns:
			Mapping: A dictionary with navigation information.
		"""
		
		...
