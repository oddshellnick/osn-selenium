from abc import ABC, abstractmethod
from typing import (
	Any,
	List,
	Literal,
	Optional
)


class AbstractTargetCDPExecutor(ABC):
	@abstractmethod
	def activate_target(self, target_id: str,) -> None:
		"""
		Activates a specific browser target, bringing it to the foreground.

		This command makes the specified target (tab or window) the active one,
		similar to clicking on a tab in a browser.

		Args:
			target_id (str): The unique ID of the target to activate.
		"""
		
		...
	
	@abstractmethod
	def attach_to_browser_target(self) -> str:
		"""
		Attaches the DevTools session to the browser itself, not a specific tab or page.

		This allows for control over browser-wide features, such as managing browser contexts,
		extensions, or global network settings.

		Returns:
			str: The `sessionId` of the newly created DevTools session for the browser.
		"""
		
		...
	
	@abstractmethod
	def attach_to_target(self, target_id: str, flatten: Optional[bool] = None) -> str:
		"""
		Attaches the DevTools session to a specific browser target.

		Attaching allows you to send CDP commands and receive events for that specific target.
		This is typically done to control a specific tab or iframe.

		Args:
			target_id (str): The unique ID of the target to attach to.
			flatten (Optional[bool]): If True, all child targets (e.g., iframes within a page)
				will also be automatically attached. Defaults to False.

		Returns:
			str: The `sessionId` of the newly created DevTools session for this target.
				This session ID is used in subsequent CDP commands to specify which session
				the command applies to.
		"""
		
		...
	
	@abstractmethod
	def close_target(self, target_id: str) -> bool:
		"""
		Closes a specific browser target (tab or window).

		Args:
			target_id (str): The unique ID of the target to close.

		Returns:
			bool: True if the target was successfully closed, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def create_browser_context(
			self,
			dispose_on_detach: Optional[bool] = None,
			proxy_server: Optional[str] = None,
			proxy_bypass_List: Optional[str] = None,
			origins_with_universal_network_access: Optional[List[str]] = None,
	) -> str:
		"""
		Sends a Chrome DevTools Protocol (CDP) command to create a new browser context.

		A browser context is an isolated environment, similar to an incognito window,
		where cookies, local storage, and other browser data are separate from
		the default context.

		Args:
			dispose_on_detach (Optional[bool]): If True, the browser context will be
				disposed of when the last target in it is detached.
			proxy_server (Optional[str]): Proxy server to use for the browser context
				(e.g., "http://localhost:8080").
			proxy_bypass_List (Optional[str]): Comma-separated List of hosts or IP addresses
				for which proxying should be bypassed.
			origins_with_universal_network_access (Optional[Sequence[str]]): A List of
				origins that are allowed to make network requests to any origin.

		Returns:
			str: The `browserContextId` of the newly created browser context.
		"""
		
		...
	
	@abstractmethod
	def create_target(
			self,
			url: str = "",
			left: Optional[int] = None,
			top: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
			window_state: Optional[Literal["normal", "minimized", "maximized", "fullscreen"]] = None,
			browser_context_id: Optional[str] = None,
			enable_begin_frame_control: Optional[bool] = None,
			new_window: Optional[bool] = None,
			background: Optional[bool] = None,
			for_tab: Optional[bool] = None,
			hidden: Optional[bool] = None,
	) -> str:
		"""
		Sends a Chrome DevTools Protocol (CDP) command to create a new browser target (tab or window).

		This method wraps the `Target.createTarget` CDP command, allowing for the creation
		of new browsing contexts with various configurations such as URL, dimensions,
		window state, and association with a specific browser context.

		Args:
			url (str): The URL to open in the new target. Defaults to an empty string,
				which typically opens a blank page.
			left (Optional[int]): The x-coordinate (left edge) of the new window/tab.
				Only applicable if `new_window` is True.
			top (Optional[int]): The y-coordinate (top edge) of the new window/tab.
				Only applicable if `new_window` is True.
			width (Optional[int]): The width of the new window/tab in pixels.
				Only applicable if `new_window` is True.
			height (Optional[int]): The height of the new window/tab in pixels.
				Only applicable if `new_window` is True.
			window_state (Optional[Literal["normal", "minimized", "maximized", "fullscreen"]]): The desired state of the new window.
				Only applicable if `new_window` is True.
			browser_context_id (Optional[str]): If specified, the new target will be
				created in the browser context with this ID. This is useful for
				incognito modes or separate user profiles.
			enable_begin_frame_control (Optional[bool]): Whether to enable BeginFrame control
				for the new target. This is an advanced feature for precise rendering control.
			new_window (Optional[bool]): If True, the target will be opened in a new browser window.
				If False or None, it will typically open as a new tab.
			background (Optional[bool]): If True, the new target will be opened in the background
				without immediately gaining focus.
			for_tab (Optional[bool]): If True, indicates that the target is intended to be a tab.
				This parameter is often used in conjunction with `new_window=False`.
			hidden (Optional[bool]): If True, the new target will be created but not immediately
				visible.

		Returns:
			str: The `targetId` of the newly created browser target. This ID is essential
				for interacting with the new target via other CDP commands.
		"""
		
		...
	
	@abstractmethod
	def detach_from_target(self, session_id: Optional[str] = None, target_id: Optional[str] = None) -> None:
		"""
		Detaches the DevTools session from a specific target.

		Detaching stops the ability to send CDP commands and receive events for that target
		via the specified session. Either `session_id` or `target_id` must be provided.

		Args:
			session_id (Optional[str]): The ID of the DevTools session to detach.
			target_id (Optional[str]): The ID of the target from which to detach.
				If `session_id` is not provided, this ID is used.
		"""
		
		...
	
	@abstractmethod
	def dispose_browser_context(self, browser_context_id: str) -> None:
		"""
		Disposes of an existing browser context.

		This closes all targets (tabs/windows) associated with the specified browser context
		and clears all associated data (e.g., cookies, local storage).

		Args:
			browser_context_id (str): The ID of the browser context to dispose of.
		"""
		
		...
	
	@abstractmethod
	def expose_dev_tools_protocol(
			self,
			target_id: str,
			binding_name: Optional[str] = None,
			inherit_permissions: Optional[bool] = None,
	) -> None:
		"""
		Exposes the DevTools Protocol API to the JavaScript context of a target.

		This allows JavaScript running within the target to directly interact with
		the DevTools Protocol by calling methods like `DevTools.evaluate` or `DevTools.send`.

		Args:
			target_id (str): The unique ID of the target to expose the protocol to.
			binding_name (Optional[str]): The name of the global object that will be
				exposed in the target's JavaScript context (default is "DevTools").
			inherit_permissions (Optional[bool]): If True, the exposed protocol will
				inherit permissions from the current DevTools session.
		"""
		
		...
	
	@abstractmethod
	def get_browser_contexts(self) -> List[str]:
		"""
		Retrieves a List of all existing browser context IDs.

		Returns:
			List[str]: A List of strings, where each string is the unique ID of a browser context.

		"""
		
		...
	
	@abstractmethod
	def get_target_info(self, target_id: Optional[str] = None) -> Any:
		"""
		Retrieves detailed information about a specific target.

		If `target_id` is not provided, it typically returns information about the
		current default target or the browser target if no specific target is active.

		Args:
			target_id (Optional[str]): The unique ID of the target to get information for.
				If None, information about the current or default target is returned.

		Returns:
			Any: The `TargetInfo` object.
		"""
		
		...
	
	@abstractmethod
	def get_targets(self, filter_: Optional[List[Any]] = None) -> Any:
		"""
		Retrieves a List of all available browser targets.

		This command can optionally filter the returned targets by type or other criteria.

		Args:
			filter_ (Optional[Sequence[Any]]): A List of target types or other filter criteria
				to narrow down the results. For example, `["page", "iframe"]` to get only
				pages and iframes.

		Returns:
			Any: A List of `TargetInfo` objects.
		"""
		
		...
	
	@abstractmethod
	def send_message_to_target(
			self,
			message: str,
			session_id: Optional[str] = None,
			target_id: Optional[str] = None,
	) -> None:
		"""
		Sends a raw DevTools Protocol message to a specific target.

		This is a low-level command for sending arbitrary CDP messages.
		Either `session_id` or `target_id` must be provided.

		Args:
			message (str): The raw JSON string of the CDP message to send.
				This message should conform to the CDP message format (e.g., `{"id": 1, "method": "Page.reload", "params": {}}`).
			session_id (Optional[str]): The ID of the DevTools session to send the message through.
			target_id (Optional[str]): The ID of the target to send the message to.
				If `session_id` is not provided, this ID is used.
		"""
		
		...
