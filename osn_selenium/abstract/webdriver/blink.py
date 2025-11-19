import pathlib
from abc import abstractmethod
from typing import Any, Mapping, Optional, Sequence, Union

from selenium.webdriver.chromium.webdriver import ChromiumDriver as legacyWebDriver

from osn_selenium.types import WindowRect
from osn_selenium.flags.utils.blink import BlinkFlags
from osn_selenium.abstract.webdriver.base import AbstractWebDriver


class AbstractBlinkWebDriver(AbstractWebDriver):
    """
    Abstract base class for a WebDriver for Blink-based browsers (e.g., Chrome, Edge).

    This class extends AbstractWebDriver with functionality specific to Blink-based browsers,
    such as managing browser executables, remote debugging ports, and other Chromium-specific features.
    """

    @property
    @abstractmethod
    def driver(self) -> Optional[legacyWebDriver]:
        """
        Gets the underlying Selenium WebDriver instance.

        This property provides direct access to the ChromiumDriver object
        that is being controlled, allowing for direct Selenium operations if needed.

        Returns:
            Optional[legacyWebDriver]: The active WebDriver instance, or None if not active.
        """
        ...

    @property
    @abstractmethod
    def debugging_port(self) -> Optional[int]:
        """
        Gets the currently set debugging port.

        Retrieves the debugging port number that the browser instance is configured to use.

        Returns:
            Optional[int]: The debugging port number, or None if not set.
        """
        ...

    @property
    @abstractmethod
    def debugging_ip(self) -> Optional[str]:
        """
        Gets the IP address part of the debugger address.

        Returns:
            Optional[str]: The IP address of the debugger, or None if not set.
        """
        ...

    @property
    @abstractmethod
    def browser_exe(self) -> Optional[Union[str, pathlib.Path]]:
        """
        Gets the path to the browser executable.

        Returns:
            Optional[Union[str, pathlib.Path]]: The path to the browser executable.
        """
        ...

    @abstractmethod
    def update_settings(
        self,
        flags: Optional[BlinkFlags] = None,
        browser_exe: Optional[Union[str, pathlib.Path]] = None,
        browser_name_in_system: Optional[str] = None,
        use_browser_exe: Optional[bool] = None,
        start_page_url: Optional[str] = None,
        window_rect: Optional[WindowRect] = None,
    ) -> None:
        """
        Updates various browser settings selectively without resetting others.

        This method allows for dynamic updating of browser settings. Only the settings
        for which a non-None value is provided will be updated.

        Args:
            flags (Optional[BlinkFlags]): New browser flags to update.
            browser_exe (Optional[Union[str, pathlib.Path]]): The new path to the browser executable.
            browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Chrome", "Edge").
            use_browser_exe (Optional[bool]): Controls the automatic detection of the browser executable.
            start_page_url (Optional[str]): The new URL for the browser to open on start.
            window_rect (Optional[WindowRect]): The new window size and position settings.
        """
        ...

    @abstractmethod
    def stop_casting(self, sink_name: str) -> Mapping[str, Any]:
        """
        Stops casting to a specific sink.

        Args:
            sink_name (str): The name of the sink to stop casting to.

        Returns:
            Mapping[str, Any]: A dictionary containing the result of the operation.
        """
        ...

    @abstractmethod
    def start_webdriver(
        self,
        flags: Optional[BlinkFlags] = None,
        browser_exe: Optional[Union[str, pathlib.Path]] = None,
        browser_name_in_system: Optional[str] = None,
        use_browser_exe: Optional[bool] = None,
        start_page_url: Optional[str] = None,
        window_rect: Optional[WindowRect] = None,
    ) -> None:
        """
        Starts the WebDriver service and the browser session.

        Initializes and starts the WebDriver instance and the associated browser process.

        Args:
            flags (Optional[BlinkFlags]): Override flags for this start.
            browser_exe (Optional[Union[str, pathlib.Path]]): Override browser executable path for this start.
            browser_name_in_system (Optional[str]): Override browser name for auto-detection for this start.
            use_browser_exe (Optional[bool]): Override auto-detection behavior for this start.
            start_page_url (Optional[str]): Override start page URL for this start.
            window_rect (Optional[WindowRect]): Override window rectangle for this start.
        """
        ...

    @abstractmethod
    def start_tab_mirroring(self, sink_name: str) -> Mapping[str, Any]:
        """
        Starts mirroring the current tab to a specific sink.

        Args:
            sink_name (str): The name of the sink to start mirroring to.

        Returns:
            Mapping[str, Any]: A dictionary containing the result of the operation.
        """
        ...

    @abstractmethod
    def start_desktop_mirroring(self, sink_name: str) -> Mapping[str, Any]:
        """
        Starts mirroring the desktop to a specific sink.

        Args:
            sink_name (str): The name of the sink to start mirroring to.

        Returns:
            Mapping[str, Any]: A dictionary containing the result of the operation.
        """
        ...

    @abstractmethod
    def set_start_page_url(self, start_page_url: str) -> None:
        """
        Sets the URL that the browser will open upon starting.

        Args:
            start_page_url (str): The URL to set as the start page.
        """
        ...

    @abstractmethod
    def set_sink_to_use(self, sink_name: str) -> Mapping:
        """
        Sets the sink to be used for casting.

        Args:
            sink_name (str): The name of the sink to use.

        Returns:
            Mapping: A dictionary containing the result of the operation.
        """
        ...

    @abstractmethod
    def set_permissions(self, name: str, value: str) -> None:
        """
        Sets a permission for the current context.

        Args:
            name (str): The name of the permission to set.
            value (str): The value to set for the permission (e.g., 'granted', 'denied').
        """
        ...

    @abstractmethod
    def set_network_conditions(self, **network_conditions: Mapping[str, Any]) -> None:
        """
        Sets network emulation conditions.

        Args:
            **network_conditions (Mapping[str, Any]): A dictionary of network conditions to set.
        """
        ...

    @abstractmethod
    def reset_settings(
        self,
        flags: Optional[BlinkFlags] = None,
        browser_exe: Optional[Union[str, pathlib.Path]] = None,
        browser_name_in_system: Optional[str] = None,
        use_browser_exe: Optional[bool] = None,
        start_page_url: str = "",
        window_rect: Optional[WindowRect] = None,
    ) -> None:
        """
        Resets various configurable browser settings to their specified or default values.

        This method can only be called when the browser session is not active.

        Args:
            flags (Optional[BlinkFlags]): New browser flags to apply. If None, flags are cleared.
            browser_exe (Optional[Union[str, pathlib.Path]]): The explicit path to the browser executable.
            browser_name_in_system (Optional[str]): The common name of the browser for auto-detection.
            use_browser_exe (Optional[bool]): Controls automatic detection of the browser executable.
            start_page_url (str): The URL that the browser will open on start. Defaults to an empty string.
            window_rect (Optional[WindowRect]): The initial window size and position settings.
        """
        ...

    @abstractmethod
    def restart_webdriver(
        self,
        flags: Optional[BlinkFlags] = None,
        browser_exe: Optional[Union[str, pathlib.Path]] = None,
        browser_name_in_system: Optional[str] = None,
        use_browser_exe: Optional[bool] = None,
        start_page_url: Optional[str] = None,
        window_rect: Optional[WindowRect] = None,
    ) -> None:
        """
        Restarts the WebDriver and browser session gracefully.

        Performs a clean restart by closing the existing session and then initiating a new one
        with potentially updated settings.

        Args:
            flags (Optional[BlinkFlags]): Override flags for the new session.
            browser_exe (Optional[Union[str, pathlib.Path]]): Override browser executable for the new session.
            browser_name_in_system (Optional[str]): Override browser name for auto-detection.
            use_browser_exe (Optional[bool]): Override auto-detection behavior for the new session.
            start_page_url (Optional[str]): Override start page URL for the new session.
            window_rect (Optional[WindowRect]): Override window rectangle for the new session.
        """
        ...

    @abstractmethod
    def log_types(self) -> Any:
        """
        Gets the available log types.

        Returns:
            Any: A list of available log types.
        """
        ...

    @abstractmethod
    def launch_app(self, id: str) -> Mapping[str, Any]:
        """
        Launches a Chrome app by its ID.

        Args:
            id (str): The ID of the app to launch.

        Returns:
            Mapping[str, Any]: A dictionary containing the result of the operation.
        """
        ...

    @abstractmethod
    def get_sinks(self) -> Sequence:
        """
        Gets a list of available sinks for casting.

        Returns:
            Sequence: A list of available sinks.
        """
        ...

    @abstractmethod
    def get_network_conditions(self) -> Mapping[str, Any]:
        """
        Gets the current network emulation conditions.

        Returns:
            Mapping[str, Any]: A dictionary of the current network conditions.
        """
        ...

    @abstractmethod
    def get_log(self, log_type: str) -> Any:
        """
        Gets the log for a given log type.

        Args:
            log_type (str): The type of log to retrieve.

        Returns:
            Any: The log entries.
        """
        ...

    @abstractmethod
    def get_issue_message(self) -> Any:
        """
        Gets issue messages from the browser.

        Returns:
            Any: The issue messages.
        """
        ...

    @abstractmethod
    def delete_network_conditions(self) -> None:
        """
        Deletes the current network emulation conditions, resetting them to default.
        """
        ...
