# osn-selenium: A robust and human-like Selenium WebDriver management library with Trio asynchronous support

`osn-selenium` is a comprehensive Python library designed to elevate browser automation with Selenium WebDriver. It focuses on simulating human-like interactions, enabling efficient asynchronous operations, and providing deep integration with the Chrome DevTools Protocol (CDP). This library offers a structured and extensible foundation for building reliable and resilient web automation scripts, featuring advanced action chains, dynamic timeout management, and seamless concurrency support via Trio. Additionally, it includes utilities for system-level browser detection and WebDriver management.

## Technologies


| Name            | Badge                                                                                                                                | Description                                                                                                                |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Python          | [![Python](https://img.shields.io/badge/Python%2DPython?style=flat&logo=python&color=%231f4361)](https://www.python.org/)            | The core programming language used for the library.                                                                        |
| Selenium        | [![Selenium](https://img.shields.io/badge/Selenium%2DSelenium?style=flat&logo=selenium&color=%23408631)](https://www.selenium.dev/)  | The underlying web automation framework for controlling browsers.                                                          |
| Trio            | [![Trio](https://img.shields.io/badge/Trio%2DTrio?style=flat&color=%23d2e7fa)](https://github.com/python-trio/trio)                  | Used for managing asynchronous operations, especially for the Chrome DevTools Protocol (CDP) event handling.               |
| Pandas          | [![Pandas](https://img.shields.io/badge/Pandas%2DPandas?style=flat&logo=pandas&color=%23130654)](https://pandas.pydata.org/)         | Used internally for processing network and process data tables on Windows.                                                 |


## Key Features

*   **Asynchronous WebDriver Operations**:
    *   Seamless integration with the Trio concurrency library, allowing synchronous Selenium calls to run in a non-blocking manner.
    *   `TrioBrowserWebDriverWrapper` provides awaitable versions of all WebDriver methods.
*   **Human-like Interactions**:
    *   Advanced action chains for simulating natural mouse movements (`build_hm_move_action`, `build_hm_move_to_element_action`).
    *   Human-like scrolling (`build_hm_scroll_action`, `build_hm_scroll_to_element_action`).
    *   Realistic text input simulation (`build_hm_text_input_action`).
*   **Chrome DevTools Protocol (CDP) Integration**:
    *   Functions as an `async with` context manager, ensuring proper setup and teardown of CDP connections.
    *   Direct execution of CDP commands (`execute_cdp_cmd`) with configurable error handling.
    *   Convenience methods for common CDP operations like target management (`cmd_create_target`, `cmd_attach_to_target`).
    *   Dynamic discovery and attachment to new browser targets (tabs, iframes, service workers).
    *   Flexible event handling system with configurable handlers for various CDP domains (e.g., `Fetch` for network interception).
*   **Browser Flag Management**:
    *   Structured management of browser arguments, experimental options, and attributes using `BrowserFlagsManager` and its specialized subclasses (`BlinkFlagsManager`, `ChromeFlagsManager`, `EdgeFlagsManager`, `YandexFlagsManager`).
    *   Support for setting and updating flags dynamically, including Blink-specific features.
*   **Window and Tab Management**:
    *   Methods for opening new tabs, switching between windows, and closing specific windows or all windows.
*   **Cookie and Credential Management**:
    *   Adding, deleting, and retrieving browser cookies.
    *   WebAuthn (FedCM) support for managing virtual authenticators and credentials.
*   **Screenshot Capabilities**:
    *   Saving screenshots to file or retrieving them as Base64/PNG bytes.
*   **Captcha Worker Integration**:
    *   Ability to register and run custom captcha detection and solving functions.
*   **Dynamic Timeout Management**:
    *   Configurable implicit wait, page load, and script timeouts, with optional random delays for human-like behavior.
*   **Element Interaction Utilities**:
    *   Finding elements within a parent or globally.
    *   Checking element visibility within the viewport.
    *   Retrieving element CSS styles and positions.
*   **Browser-Specific Implementations**:
    *   Dedicated WebDriver classes for Chrome (`ChromeWebDriver`), Edge (`EdgeWebDriver`), and Yandex Browser (`YandexWebDriver`), inheriting common Blink-based functionalities.
    *   Automatic browser executable detection for supported browsers on Windows.
*   **System Browser Information Retrieval**:
    *   Detects and lists installed web browsers on the operating system.
    *   Retrieves precise version numbers and executable paths for detected browsers.
    *   Checks the version of WebDriver executables for compatibility.
*   **Comprehensive Logging**:
    *   Detailed logging system with per-target and overall statistics.
    *   Configurable log levels and target type filters for fine-grained control over what gets logged.
    *   Logs to memory, console, and optional file output, including full tracebacks for errors.
*   **Background Task Execution**:
    *   Ability to run custom asynchronous background tasks for each attached `DevToolsTarget`.

## Installation

1.  Install library:
    *   **With pip:**
        ```bash
        pip install osn-selenium
        ```

    *   **With git:**
        ```bash
        pip install git+https://github.com/oddshellnick/osn-selenium.git
        ```
        *(Ensure you have git installed)*

2.  **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure `pywin32` is installed for Windows-specific functionality if not automatically handled by `requirements.txt`)*

## Usage

Here are some examples of how to use `osn-selenium`:

### Basic Asynchronous Browser Navigation

This example demonstrates how to initialize a `ChromeWebDriver`, wrap it for Trio, and perform basic asynchronous navigation and element interaction.

```python
import trio
from selenium.webdriver.common.by import By
from osn_selenium.webdrivers.Chrome.webdriver import ChromeWebDriver

async def main():
    # Initialize ChromeWebDriver with the path to your chromedriver executable
    # You might need to download chromedriver matching your Chrome browser version
    # from https://chromedriver.chromium.org/downloads
    driver = ChromeWebDriver(webdriver_path="/path/to/your/chromedriver.exe") 
    
    # Wrap the synchronous driver for asynchronous operations with Trio
    async_driver = driver.to_wrapper()

    try:
        await async_driver.start_webdriver(start_page_url="https://www.example.com")
        print(f"WebDriver active: {async_driver.is_active}")
        print(f"Current URL: {async_driver.current_url}")

        # Find an element asynchronously
        element = await async_driver.find_web_element(By.TAG_NAME, "h1")
        print(f"Found element text: {element.text}")

        # Perform a human-like click action on the element
        action_chain = await async_driver.click_action(element=element)
        action_chain.perform() # Don't forget to perform the action chain
        print("Clicked the H1 element.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await async_driver.close_webdriver()
        print("WebDriver closed.")

if __name__ == "__main__":
    trio.run(main)
```

### Intercepting and Modifying Network Requests (Fetch Domain)

This example demonstrates how to use the `Fetch` domain to intercept requests and modify their headers.

```python
import trio
from pathlib import Path
from osn_selenium.webdrivers.Chrome.webdriver import ChromeWebDriver
from osn_selenium.dev_tools.manager import DevToolsSettings, DevToolsTarget
from osn_selenium.dev_tools.logger import LoggerSettings
from osn_selenium.dev_tools.domains.fetch import (
    FetchSettings,
    FetchEnableKwargsSettings,
    FetchHandlersSettings,
    RequestPausedSettings,
    RequestPausedActionsHandlerSettings,
    RequestPausedActionsSettings,
    ContinueRequestSettings,
    ContinueRequestHandlersSettings,
)
from osn_selenium.dev_tools.domains_default.fetch import HeaderInstance
from osn_selenium.dev_tools.domains.abstract import ParameterHandler
from osn_selenium.dev_tools.domains import DomainsSettings
from osn_selenium.dev_tools.utils import TargetFilter
from typing import Any, Sequence, Literal

# 1. Define a custom parameter handler for headers
async def custom_headers_param_handler(
    self: DevToolsTarget,
    ready_event: trio.Event,
    headers_to_modify: dict[str, HeaderInstance],
    event: Any,
    kwargs: dict[str, Any]
):
    """Modifies request headers based on predefined instructions."""
    header_entry_class = await self.get_devtools_object("fetch.HeaderEntry")
    current_headers = {h.name.lower(): h.value for h in event.request.headers} # Normalize names

    new_headers_list = []
    for name, value in event.request.headers.items():
        if name.lower() not in headers_to_modify: # Keep headers not explicitly modified
            new_headers_list.append(header_entry_class(name=name, value=value))

    for header_name, instance in headers_to_modify.items():
        value = instance["value"]
        instruction = instance["instruction"]
        
        if instruction == "set":
            new_headers_list.append(header_entry_class(name=header_name, value=str(value)))
        elif instruction == "set_exist" and header_name.lower() in current_headers:
            new_headers_list.append(header_entry_class(name=header_name, value=str(value)))
        # "remove" is handled by not re-adding the header

    kwargs["headers"] = new_headers_list
    ready_event.set()

# 2. Define a custom choose_action_func for RequestPaused
def choose_action_for_request(
    self: DevToolsTarget, 
    event: Any
) -> Sequence[Literal["continue_request", "fail_request", "fulfill_request", "continue_response"]]:
    """Decides whether to continue or modify a request based on its URL."""
    if "example.com" in event.request.url:
        return ["continue_request"] # Modify and continue
    return ["continue_request"] # Default: just continue

async def main():
    # Define custom headers to add/modify/remove
    custom_headers = {
        "X-Custom-Header": HeaderInstance(value="MyCustomValue", instruction="set"),
        "User-Agent": HeaderInstance(value="Mozilla/5.0 (CustomAgent)", instruction="set"),
        "Accept-Encoding": HeaderInstance(value="", instruction="remove")
    }

    # Configure Fetch domain settings
    fetch_settings = FetchSettings(
        enable_func_kwargs=FetchEnableKwargsSettings(
            patterns=[{"urlPattern": "*", "requestStage": "Request"}], # Intercept all requests at Request stage
            handle_auth_requests=False
        ),
        handlers=FetchHandlersSettings(
            request_paused=RequestPausedSettings(
                actions_handler=RequestPausedActionsHandlerSettings(
                    choose_action_func=choose_action_for_request,
                    actions=RequestPausedActionsSettings(
                        continue_request=ContinueRequestSettings(
                            parameters_handlers=ContinueRequestHandlersSettings(
                                headers=ParameterHandler(
                                        func=custom_headers_param_handler,
                                        instances=custom_headers
                                ),
                            )
                        )
                    )
                )
            )
        )
    )

    devtools_settings = DevToolsSettings(
        new_targets_filter=[TargetFilter(type_="page"), TargetFilter(type_="iframe")],
        logger_settings=LoggerSettings(log_dir_path=Path("./devtools_logs"), renew_log=True),
    )

    driver = ChromeWebDriver(
        webdriver_path="/path/to/your/chromedriver.exe",
        devtools_settings=devtools_settings
    )
    driver.dev_tools.set_domains_handlers(DomainsSettings(fetch=fetch_settings))
    async_driver = driver.to_wrapper()

    try:
        await async_driver.start_webdriver()
        
        async with driver.dev_tools:
            print("DevTools context entered. Fetch interception enabled.")
            await async_driver.search_url("https://httpbin.org/headers") # A site that echoes headers
            await trio.sleep(3) # Give time for request and logging
            
            # You can open the devtools_logs/__MAIN__.txt and target-specific logs
            # to see the "RequestPaused" events and the modified headers.

        print("DevTools context exited.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await async_driver.close_webdriver()
        print("WebDriver closed.")

if __name__ == "__main__":
    trio.run(main)
```

## Classes and Functions

This section provides a detailed overview of the classes and functions organized by their respective packages and modules within the `osn-selenium` library.

### Root Level (`osn_selenium/`)
*   `__init__.py`:
    *   `CaptchaWorkerSettings(TypedDict)`: Typed dictionary for defining a captcha worker.
*   `types.py`:
    *   `WindowRect`: Represents a window rectangle with x, y, width, and height.
    *   `Size(TypedDict)`: Represents a dictionary structure defining the size.
    *   `Rectangle(TypedDict)`: Represents a dictionary structure defining the properties of a rectangle.
    *   `Position(TypedDict)`: Represents a dictionary structure defining the position.
*   `errors.py`:
    *   `PlatformNotSupportedError(Exception)`: Custom exception raised when the current platform is not supported.

### 'captcha_workers' (`osn_selenium/captcha_workers/`)
*   `__init__.py`:
    *   `CaptchaWorkerSettings(TypedDict)`: Typed dictionary for defining a captcha worker.

### `browsers_handler` (`osn_selenium/browsers_handler/`)
*   `__init__.py`:
    *   `get_installed_browsers()`: Retrieves a list of installed browsers on the system.
    *   `get_version_of_browser(...)`: Retrieves the version of a specific installed browser by name.
    *   `get_path_to_browser(...)`: Retrieves the installation path of a specific installed browser by name.
*   `types.py`:
    *   `Browser(TypedDict)`: Represents a browser installed on the system.
*   `_windows.py`:
    *   `get_webdriver_version(...)`: Retrieves the version of a given WebDriver executable.
    *   `get_browser_version(...)`: Retrieves the version of a browser given its file path (Windows-specific).
    *   `get_installed_browsers_win32()`: Retrieves a list of installed browsers on a Windows system by querying the registry.

### `webdrivers` (`osn_selenium/webdrivers/`)
*   `_functions.py`:
    *   `text_input_to_parts(text)`: Breaks down a text string into smaller parts for simulating human-like typing.
    *   `str_adding_validation_function(value)`: Validates if a value is a non-empty string.
    *   `scroll_to_parts(start_position, end_position)`: Calculates a sequence of smaller scroll steps with durations.
    *   `read_js_scripts()`: Reads JavaScript scripts from files.
    *   `path_adding_validation_function(value)`: Validates if a value is a non-empty string or a `pathlib.Path` object.
    *   `optional_bool_adding_validation_function(value)`: Validates if a value is a boolean or `None`.
    *   `move_to_parts(start_position, end_position)`: Calculates a sequence of smaller move steps with durations for human-like mouse movement.
    *   `int_adding_validation_function(value)`: Validates if a value is an integer.
    *   `get_found_profile_dir(data, profile_dir_command)`: Extracts the browser profile directory path from a process's command line arguments (Windows-only).
    *   `get_active_executables_table(browser_exe)`: Retrieves a table of active executables related to a specified browser, listening on localhost (Windows-only).
    *   `find_browser_previous_session(browser_exe, profile_dir_command, profile_dir)`: Finds the port number of a previously opened browser session.
    *   `build_first_start_argument(browser_exe)`: Builds the first command line argument to start a browser executable.
    *   `bool_adding_validation_function(value)`: Validates if a value is a boolean and `True`.
*   `types.py`:
    *   `_MoveStep`: Internal helper class representing a step in a movement calculation.
    *   `TextInputPart`: Represents a segment of text input with an associated duration.
    *   `ScrollDelta`: Represents the change in scroll position (`dx`, `dy`).
    *   `ActionPoint`: Represents a 2D point with integer coordinates (`x`, `y`).
    *   `ScrollPart`: Represents a segment of a simulated scroll action.
    *   `MoveOffset`: Represents a 2D offset or displacement (`dx`, `dy`).
    *   `MovePart`: Represents a segment of a simulated mouse movement.
    *   `JS_Scripts(TypedDict)`: Type definition for a collection of JavaScript script snippets.
    *   `FlagDefinition(TypedDict)`: Defines the structure for a single browser flag or option.
    *   `FlagType(TypedDict)`: Defines the callable interfaces for managing different types of browser flags.
    *   `FlagNotDefined`: Sentinel class indicating a flag definition was not found.
    *   `AutoplayPolicyType`, `LogLevelType`, `UseGLType`: Literal types for various flag values.
    *   `_any_flags_mapping`, `_any_webdriver_option_type`, `_blink_webdriver_option_type`: Generic type aliases.

#### `BaseDriver` (`osn_selenium/webdrivers/BaseDriver/`)
*   `_utils.py`:
    *   `trio_async_wrap(...)`: Decorator to wrap a synchronous function for Trio asynchronous execution.
    *   `build_cdp_kwargs(...)`: Helper function to filter out `None` values from keyword arguments.
*   `flags.py`:
    *   `BrowserExperimentalOptions(TypedDict)`: Typed dictionary for browser-agnostic experimental options.
    *   `BrowserAttributes(TypedDict)`: Typed dictionary for browser-agnostic WebDriver attributes.
    *   `BrowserArguments(TypedDict)`: Typed dictionary for browser-agnostic command-line arguments.
    *   `BrowserFlags(TypedDict)`: Comprehensive typed dictionary for all browser-agnostic flag types.
    *   `BrowserFlagsManager`: Manages browser flags (arguments, experimental options, attributes) for a generic WebDriver.
        *   `build_options_attributes(...)`: Applies configured attributes to WebDriver options.
        *   `clear_attributes()`: Clears all configured browser attributes.
        *   `remove_attribute(...)`: Removes a browser attribute.
        *   `set_attribute(...)`: Sets a browser attribute.
        *   `update_attributes(...)`: Updates browser attributes without clearing existing ones.
        *   `set_attributes(...)`: Clears existing and sets new browser attributes.
        *   `build_options_experimental_options(...)`: Adds configured experimental options to WebDriver options.
        *   `clear_experimental_options()`: Clears all configured experimental options.
        *   `remove_experimental_option(...)`: Removes an experimental option.
        *   `set_experimental_option(...)`: Sets an experimental option.
        *   `update_experimental_options(...)`: Updates experimental options without clearing existing ones.
        *   `set_experimental_options(...)`: Clears existing and sets new experimental options.
        *   `build_start_args_arguments()`: Builds a list of command-line arguments for browser startup.
        *   `build_options_arguments(...)`: Adds configured command-line arguments to WebDriver options.
        *   `clear_arguments()`: Clears all configured browser arguments.
        *   `remove_argument(...)`: Removes a browser argument.
        *   `set_argument(...)`: Sets a command-line argument.
        *   `update_arguments(...)`: Updates command-line arguments without clearing existing ones.
        *   `set_arguments(...)`: Clears existing and sets new command-line arguments.
        *   `clear_flags()`: Clears all configured flags of all types.
        *   `_renew_webdriver_options()`: Abstract method to renew WebDriver options (must be implemented by subclasses).
        *   `options (property)`: Builds and returns a WebDriver options object with all configured flags applied.
        *   `remove_option(...)`: Removes a browser option by its configuration object.
        *   `set_flags(...)`: Clears all existing flags and sets new ones.
        *   `set_option(...)`: Sets a browser option based on its configuration.
        *   `update_flags(...)`: Updates all flags without clearing existing ones.
*   `protocols.py`:
    *   `TrioWebDriverWrapperProtocol(Protocol)`: Wraps `BrowserWebDriver` methods for asynchronous execution using Trio.
*   `trio_wrapper.py`:
    *   `TrioBrowserWebDriverWrapper`: Wraps `BrowserWebDriver` methods for asynchronous execution using Trio.
*   `webdriver.py`:
    *   `BrowserWebDriver`: A base class for managing a Selenium WebDriver instance and browser interactions.
        *   `add_captcha_worker(...)`: Adds a new captcha worker.
        *   `add_cookie(...)`: Adds a single cookie.
        *   `add_credential(...)`: Adds a WebAuthn credential.
        *   `add_virtual_authenticator(options)`: Adds a virtual authenticator.
        *   `build_action_chains(...)`: Builds and returns a new Selenium `ActionChains` instance.
        *   `build_hm_move_action(...)`: Builds a human-like mouse move action sequence.
        *   `execute_js_script(...)`: Executes a JavaScript script.
        *   `get_element_rect_in_viewport(...)`: Gets element position and dimensions relative to viewport.
        *   `get_random_element_point_in_viewport(...)`: Calculates a random point within visible portion of element in viewport.
        *   `get_random_element_point(...)`: Gets coordinates of a random point within an element.
        *   `build_hm_move_to_element_action(...)`: Builds a human-like mouse move action to an element.
        *   `get_viewport_size()`: Gets current dimensions of browser's viewport.
        *   `build_hm_scroll_action(...)`: Builds a human-like scroll action sequence.
        *   `get_viewport_rect()`: Gets position and dimensions of viewport.
        *   `build_hm_scroll_to_element_action(...)`: Builds a human-like scroll action to bring an element into view.
        *   `build_hm_text_input_action(...)`: Builds a human-like text input action sequence.
        *   `captcha_workers (property)`: Gets the current list of configured captcha workers.
        *   `check_captcha(...)`: Iterates through registered captcha workers to detect and solve captchas.
        *   `check_element_in_viewport(...)`: Checks if a web element is within the browser's viewport.
        *   `click_action(...)`: Adds a click action.
        *   `click_and_hold_action(...)`: Adds a click-and-hold action.
        *   `windows_handles (property)`: Gets the handles of all open windows.
        *   `get_window_handle(...)`: Retrieves a window handle string.
        *   `switch_to_window(...)`: Switches the driver's focus to the specified browser window.
        *   `current_window_handle (property)`: Gets the current window handle.
        *   `close_window(...)`: Closes the specified browser window.
        *   `close_all_windows()`: Closes all open windows.
        *   `execute_cdp_cmd(...)`: Executes a Chrome DevTools Protocol (CDP) command.
        *   `cmd_activate_target(...)`: Activates a specific browser target (CDP).
        *   `cmd_attach_to_browser_target()`: Attaches the DevTools session to the browser itself (CDP).
        *   `cmd_attach_to_target(...)`: Attaches the DevTools session to a specific target (CDP).
        *   `cmd_close_target(...)`: Closes a specific browser target (CDP).
        *   `cmd_create_browser_context(...)`: Creates a new browser context (CDP).
        *   `cmd_create_target(...)`: Creates a new browser target (tab or window) (CDP).
        *   `cmd_detach_from_target(...)`: Detaches the DevTools session from a specific target (CDP).
        *   `cmd_dispose_browser_context(...)`: Disposes of an existing browser context (CDP).
        *   `cmd_expose_dev_tools_protocol(...)`: Exposes the DevTools Protocol API to JavaScript context (CDP).
        *   `cmd_get_browser_contexts()`: Retrieves a list of all existing browser context IDs (CDP).
        *   `cmd_get_target_info(...)`: Retrieves detailed information about a specific target (CDP).
        *   `cmd_get_targets(..._)`: Retrieves a list of all available browser targets (CDP).
        *   `cmd_send_message_to_target(...)`: Sends a raw DevTools Protocol message to a target (CDP).
        *   `context_click_action(...)`: Adds a context-click (right-click) action.
        *   `cookies (property)`: Gets all cookies visible to the current page.
        *   `current_url (property)`: Gets the current URL.
        *   `delete_all_cookies()`: Deletes all cookies.
        *   `delete_cookie(...)`: Deletes a single cookie by its name.
        *   `delete_downloadable_files()`: Deletes all downloadable files.
        *   `double_click_action(...)`: Adds a double-click action.
        *   `download_file(...)`: Downloads a file from the browser.
        *   `drag_and_drop_action(...)`: Adds a drag-and-drop action.
        *   `drag_and_drop_by_offset_action(...)`: Adds a drag-and-drop by offset action.
        *   `driver (property)`: Gets the underlying Selenium WebDriver instance.
        *   `execute_async_js_script(...)`: Executes an asynchronous JavaScript script.
        *   `fedcm (property)`: Gets the FedCM (Federated Credential Management) interface.
        *   `fedcm_dialog (property)`: Gets the FedCM dialog interface.
        *   `set_script_timeout(...)`: Sets the script timeout.
        *   `set_implicitly_wait_timeout(...)`: Sets implicit wait timeout.
        *   `set_page_load_timeout(...)`: Sets page load timeout.
        *   `set_driver_timeouts(...)`: Sets all three WebDriver timeouts.
        *   `update_times(...)`: Updates WebDriver's timeout settings with random delays.
        *   `find_inner_web_element(...)`: Finds a single web element within another element.
        *   `find_inner_web_elements(...)`: Finds multiple web elements within another element.
        *   `find_web_element(...)`: Finds a single web element on the page.
        *   `find_web_elements(...)`: Finds multiple web elements on the page.
        *   `fullscreen_window()`: Makes the current browser window full screen.
        *   `get_cookie(name)`: Gets a single cookie by its name.
        *   `get_credentials()`: Gets a list of all registered WebAuthn credentials.
        *   `get_document_scroll_size()`: Gets the total scrollable dimensions of the HTML document.
        *   `get_downloadable_files()`: Gets a list of downloadable files.
        *   `get_element_css_style(...)`: Retrieves the computed CSS style of a `WebElement`.
        *   `get_fedcm_dialog(...)`: Waits for and retrieves the FedCM dialog.
        *   `get_screenshot_as_base64()`: Gets the screenshot as a Base64 encoded string.
        *   `get_screenshot_as_file(...)`: Saves a screenshot to a specified file.
        *   `get_screenshot_as_png()`: Gets the screenshot as a PNG image in bytes.
        *   `get_vars_for_remote()`: Gets variables necessary to create a remote WebDriver instance.
        *   `get_viewport_position()`: Gets the current scroll position of the viewport.
        *   `key_down_action(...)`: Adds a key down (press and hold) action.
        *   `key_up_action(...)`: Adds a key up (release) action.
        *   `maximize_window()`: Maximizes the current browser window.
        *   `minimize_window()`: Minimizes the current browser window.
        *   `move_to_element_action(...)`: Adds a move mouse cursor action to a web element.
        *   `move_to_element_with_offset_action(...)`: Adds an action to move the mouse cursor to an offset.
        *   `open_new_tab(link)`: Opens a new tab with the given URL.
        *   `orientation (property)`: Gets/sets the current screen orientation.
        *   `page_source (property)`: Gets the HTML source code of the current page.
        *   `print_page(...)`: Prints the current page to PDF.
        *   `rect (property)`: Gets the window rectangle.
        *   `refresh_webdriver()`: Refreshes the current page.
        *   `release_action(...)`: Adds a release mouse button action.
        *   `remote_connect_driver(...)`: Connects to an existing remote WebDriver session.
        *   `remove_all_credentials()`: Removes all WebAuthn credentials.
        *   `remove_captcha_worker(...)`: Removes a captcha worker.
        *   `remove_credential(...)`: Removes a specific WebAuthn credential.
        *   `remove_virtual_authenticator()`: Removes the active virtual authenticator.
        *   `reset_captcha_workers(...)`: Resets the list of captcha workers.
        *   `set_trio_tokens_limit(...)`: Updates the Trio capacity limiter.
        *   `is_active (property)`: Checks if the WebDriver instance is currently active.
        *   `reset_settings(...)`: Resets all configurable browser settings.
        *   `_create_driver()`: Abstract method to create a WebDriver instance (must be implemented by subclasses).
        *   `update_settings(...)`: Updates various browser settings selectively.
        *   `start_webdriver(...)`: Starts the WebDriver service and the browser session.
        *   `close_webdriver()`: Closes the WebDriver instance and terminates the browser.
        *   `restart_webdriver(...)`: Restarts the WebDriver and browser session gracefully.
        *   `scroll_by_amount_action(...)`: Adds a scroll action by specified amounts.
        *   `scroll_from_origin_action(...)`: Adds a scroll action relative to a specified origin.
        *   `scroll_to_element_action(...)`: Adds an action to scroll to an element.
        *   `search_url(...)`: Opens a URL in the current browser session.
        *   `send_keys_action(...)`: Adds a send keys action to the focused element.
        *   `send_keys_to_element_action(...)`: Adds a send keys action to a specific web element.
        *   `set_captcha_worker(...)`: Adds a captcha worker configuration.
        *   `set_user_verified(...)`: Sets the user verification state for WebAuthn.
        *   `set_window_rect(...)`: Sets the browser window rectangle.
        *   `stop_window_loading()`: Stops the current page loading.
        *   `supports_fedcm (property)`: Checks if the browser supports FedCM API.
        *   `switch_to_frame(...)`: Switches the driver's focus to a frame.
        *   `to_wrapper()`: Creates a `TrioBrowserWebDriverWrapper` instance.
        *   `virtual_authenticator_id (property)`: Gets the ID of the active virtual authenticator.

#### `Blink` (`osn_selenium/webdrivers/Blink/`)
*   `flags.py`:
    *   `BlinkExperimentalOptions(BrowserExperimentalOptions)`: Extends base experimental options for Blink.
    *   `BlinkFeatures(TypedDict)`: Typed dictionary for Blink-specific feature flags.
    *   `BlinkAttributes(BrowserAttributes)`: Extends base attributes for Blink.
    *   `BlinkArguments(BrowserArguments)`: Extends base arguments for Blink.
    *   `BlinkFlags(TypedDict)`: Collection of all flag types for Blink-based browsers.
    *   `BlinkFlagsManager(BrowserFlagsManager)`: Manages flags for Blink-based browsers, adding support for Blink Features.
        *   `build_start_args_blink_features()`: Builds a list of Blink feature arguments for browser startup.
        *   `build_options_blink_features(...)`: Adds configured Blink features to WebDriver options.
        *   `clear_blink_features()`: Clears all configured Blink features.
        *   `remove_blink_feature(...)`: Removes a configured Blink feature.
        *   `set_blink_feature(...)`: Sets a Blink feature to be enabled or disabled.
        *   `update_blink_features(...)`: Updates Blink features without clearing existing ones.
        *   `set_blink_features(...)`: Clears existing and sets new Blink features.
        *   `_renew_webdriver_options()`: Abstract method to renew WebDriver options (for Blink-specific options).
        *   `browser_exe (property)`: Gets/sets the browser executable path.
        *   `build_options_arguments(...)`: Overrides to add arguments to Blink options.
        *   `build_options_attributes(...)`: Overrides to apply attributes to Blink options.
        *   `build_options_experimental_options(...)`: Overrides to add experimental options to Blink options.
        *   `build_start_args_arguments()`: Overrides to build startup arguments for Blink.
        *   `clear_flags()`: Overrides to clear all flags and reset start page URL.
        *   `options (property)`: Overrides to build and return a Blink-specific WebDriver options object.
        *   `set_arguments(...)`: Overrides to set Blink arguments.
        *   `set_attributes(...)`: Overrides to set Blink attributes.
        *   `set_experimental_options(...)`: Overrides to set Blink experimental options.
        *   `set_flags(...)`: Overrides to clear and set new flags, including Blink features.
        *   `start_args (property)`: Builds and returns a list of all command-line arguments for browser startup.
        *   `start_command (property)`: Generates the full browser start command.
        *   `start_page_url (property)`: Gets/sets the initial URL to open when the browser starts.
        *   `update_arguments(...)`: Overrides to update Blink arguments.
        *   `update_attributes(...)`: Overrides to update Blink attributes.
        *   `update_experimental_options(...)`: Overrides to update Blink experimental options.
        *   `update_flags(...)`: Overrides to update all flags, including Blink features.
*   `protocols.py`:
    *   `TrioBlinkWebDriverWrapperProtocol(TrioWebDriverWrapperProtocol)`: Wraps `BlinkWebDriver` methods for asynchronous execution.
        *   `_check_browser_exe_active()`: Checks if the WebDriver is active by verifying debugging port use.
        *   `_find_debugging_port(...)`: Finds an appropriate debugging port.
        *   `_set_debugging_port(...)`: Sets the debugging port and address.
        *   `browser_exe (property)`: Gets the path to the browser executable.
        *   `close_webdriver()`: Overrides to include process termination for Blink.
        *   `debugging_ip (property)`: Gets the IP address part of the debugger address.
        *   `debugging_port (property)`: Gets the currently set debugging port.
        *   `driver (property)`: Gets the underlying Selenium WebDriver instance (Chrome/Edge).
        *   `reset_settings(...)`: Overrides to reset Blink-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Blink-specific WebDriver.
        *   `set_start_page_url(...)`: Sets the URL that the browser will open upon starting.
        *   `start_webdriver(...)`: Overrides to start Blink-specific WebDriver.
        *   `update_settings(...)`: Overrides to update Blink-specific settings.
*   `webdriver.py`:
    *   `BlinkWebDriver(BrowserWebDriver)`: A WebDriver manager for Blink-based browsers (e.g., Chrome, Edge).
        *   `debugging_port (property)`: Gets the currently set debugging port.
        *   `browser_exe (property)`: Gets the path to the browser executable.
        *   `_find_debugging_port(...)`: Finds an appropriate debugging port.
        *   `_set_debugging_port(...)`: Sets the debugging port and address.
        *   `debugging_ip (property)`: Gets the IP address part of the debugger address.
        *   `_detect_browser_exe(...)`: Detects and sets the browser executable path.
        *   `set_start_page_url(...)`: Sets the URL that the browser will open upon starting.
        *   `reset_settings(...)`: Overrides to reset Blink-specific settings including browser executable.
        *   `_create_driver()`: Abstract method to create a WebDriver instance (must be implemented by subclasses).
        *   `_check_browser_exe_active()`: Checks if the WebDriver is active by verifying if the debugging port is in use.
        *   `update_settings(...)`: Overrides to update Blink-specific settings.
        *   `driver (property)`: Overrides to get the underlying Selenium WebDriver instance (Chrome/Edge).
        *   `start_webdriver(...)`: Overrides to start the WebDriver service and browser session, including process management.
        *   `close_webdriver()`: Overrides to close WebDriver and terminate browser process.
        *   `restart_webdriver(...)`: Overrides to restart Blink-specific WebDriver.
        *   `to_wrapper()`: Overrides to create a `TrioBlinkWebDriverWrapperProtocol` instance.

#### `Chrome` (`osn_selenium/webdrivers/Chrome/`)
*   `flags.py`:
    *   `ChromeFlagsManager(BlinkFlagsManager)`: Manages Chrome Browser-specific options.
        *   `_renew_webdriver_options()`: Creates and returns a new `Options` object (ChromeOptions).
    *   `ChromeAttributes(BlinkAttributes)`: Typed dictionary for Chrome-specific WebDriver attributes.
    *   `ChromeExperimentalOptions(BlinkExperimentalOptions)`: Typed dictionary for Chrome-specific experimental options.
    *   `ChromeArguments(BlinkArguments)`: Typed dictionary for Chrome-specific command-line arguments.
    *   `ChromeFlags(TypedDict)`: Collection of all flag types for Chrome browsers.
*   `protocols.py`:
    *   `TrioChromeWebDriverWrapperProtocol(TrioBlinkWebDriverWrapperProtocol)`: Wraps `ChromeWebDriver` methods for asynchronous execution.
        *   `driver (property)`: Gets the underlying Selenium `webdriver.Chrome` instance.
        *   `reset_settings(...)`: Overrides to reset Chrome-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Chrome-specific WebDriver.
        *   `start_webdriver(...)`: Overrides to start Chrome-specific WebDriver.
        *   `update_settings(...)`: Overrides to update Chrome-specific settings.
*   `webdriver.py`:
    *   `ChromeWebDriver(BlinkWebDriver)`: Manages a Chrome Browser session using Selenium WebDriver.
        *   `_create_driver()`: Creates the Chrome WebDriver instance (`webdriver.Chrome`).
        *   `driver (property)`: Gets the underlying Selenium `webdriver.Chrome` instance.
        *   `reset_settings(...)`: Overrides to reset Chrome-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Chrome-specific WebDriver.
        *   `start_webdriver(...)`: Overrides to start Chrome-specific WebDriver.
        *   `to_wrapper()`: Overrides to create a `TrioChromeWebDriverWrapperProtocol` instance.
        *   `update_settings(...)`: Overrides to update Chrome-specific settings.

#### `Edge` (`osn_selenium/webdrivers/Edge/`)
*   `flags.py`:
    *   `EdgeFlagsManager(BlinkFlagsManager)`: Manages Edge Browser-specific options.
        *   `_renew_webdriver_options()`: Creates and returns a new `Options` object (EdgeOptions).
    *   `EdgeAttributes(BlinkAttributes)`: Typed dictionary for Edge-specific WebDriver attributes.
    *   `EdgeExperimentalOptions(BlinkExperimentalOptions)`: Typed dictionary for Edge-specific experimental options.
    *   `EdgeArguments(BlinkArguments)`: Typed dictionary for Edge-specific command-line arguments.
    *   `EdgeFlags(TypedDict)`: Collection of all flag types for Edge browsers.
*   `protocols.py`:
    *   `TrioEdgeWebDriverWrapperProtocol(TrioBlinkWebDriverWrapperProtocol)`: Wraps `EdgeWebDriver` methods for asynchronous execution.
        *   `driver (property)`: Gets the underlying Selenium `webdriver.Edge` instance.
        *   `reset_settings(...)`: Overrides to reset Edge-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Edge-specific WebDriver.
        *   `start_webdriver(...)`: Overrides to start Edge-specific WebDriver.
        *   `update_settings(...)`: Overrides to update Edge-specific settings.
*   `webdriver.py`:
    *   `EdgeWebDriver(BlinkWebDriver)`: Manages an Edge Browser session using Selenium WebDriver.
        *   `_create_driver()`: Creates the Edge WebDriver instance (`webdriver.Edge`).
        *   `driver (property)`: Gets the underlying Selenium `webdriver.Edge` instance.
        *   `reset_settings(...)`: Overrides to reset Edge-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Edge-specific WebDriver.
        *   `start_webdriver(...)`: Overrides to start Edge-specific WebDriver.
        *   `to_wrapper()`: Overrides to create a `TrioEdgeWebDriverWrapperProtocol` instance.
        *   `update_settings(...)`: Overrides to update Edge-specific settings.

#### `Yandex` (`osn_selenium/webdrivers/Yandex/`)
*   `flags.py`:
    *   `YandexFlagsManager(ChromeFlagsManager)`: Manages Yandex Browser-specific options.
        *   `_renew_webdriver_options()`: Creates and returns a new `Options` object (ChromeOptions, compatible with Yandex).
    *   `YandexAttributes(ChromeAttributes)`: Typed dictionary for Yandex-specific WebDriver attributes.
    *   `YandexExperimentalOptions(ChromeExperimentalOptions)`: Typed dictionary for Yandex-specific experimental options.
    *   `YandexArguments(ChromeArguments)`: Typed dictionary for Yandex-specific command-line arguments.
    *   `YandexFlags(TypedDict)`: Collection of all flag types for Yandex browsers.
*   `protocols.py`:
    *   `TrioYandexWebDriverWrapperProtocol(TrioChromeWebDriverWrapperProtocol)`: Wraps `YandexWebDriver` methods for asynchronous execution.
        *   `reset_settings(...)`: Overrides to reset Yandex-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Yandex-specific WebDriver.
        *   `start_webdriver(...)`: Overrides to start Yandex-specific WebDriver.
        *   `update_settings(...)`: Overrides to update Yandex-specific settings.
*   `webdriver.py`:
    *   `YandexWebDriver(ChromeWebDriver)`: Manages a Yandex Browser session using Selenium WebDriver.
        *   `reset_settings(...)`: Overrides to reset Yandex-specific settings.
        *   `restart_webdriver(...)`: Overrides to restart Yandex-specific WebDriver.
        *   `start_webdriver(...)`: Overrides to start Yandex-specific WebDriver.
        *   `to_wrapper()`: Overrides to create a `TrioYandexWebDriverWrapperProtocol` instance.
        *   `update_settings(...)`: Overrides to update Yandex-specific settings.

### `dev_tools` (`osn_selenium/dev_tools/`)
*   `_types.py`:
    *   `devtools_background_func_type`: Type alias for an asynchronous background task function for `DevToolsTarget`.
    *   `LogLevelsType`: Literal type for various log levels used in the logging system.
*   `errors.py`:
    *   `WrongHandlerSettingsTypeError(Exception)`: Raised when event handler settings type is incorrect.
    *   `WrongHandlerSettingsError(Exception)`: Raised when event handler settings are incorrect (e.g., missing required keys).
    *   `CantEnterDevToolsContextError(Exception)`: Raised when unable to enter the DevTools context.
    *   `BidiConnectionNotEstablishedError(Exception)`: Raised when a BiDi connection is required but not established.
    *   `trio_end_exceptions`: Tuple of Trio exceptions indicating channel/resource closure.
    *   `cdp_end_exceptions`: Tuple of CDP-related connection closure exceptions.
*   `utils.py`:
    *   `warn_if_active(...)`: Decorator to warn if DevTools operations are attempted while DevTools is active.
    *   `wait_one(...)`: Waits for the first of multiple Trio events to be set.
    *   `log_on_error(...)`: Decorator that logs any `BaseException` raised by the decorated async function.
    *   `extract_exception_trace(...)`: Extracts a comprehensive traceback string for an exception.
    *   `log_exception(...)`: Logs the full traceback of an exception at the ERROR level.
    *   `ExceptionThrown`: A wrapper class to indicate that an exception was thrown during an operation.
    *   `execute_cdp_command(...)`: Executes a Chrome DevTools Protocol (CDP) command with specified error handling.
    *   `_validate_log_filter(...)`: Creates a callable filter function based on the specified filter mode and values.
    *   `_validate_type_filter(...)`: Validates a target type against a given filter.
    *   `_prepare_log_dir(...)`: Prepares the log directory for file logging.
    *   `_background_task_decorator(...)`: Decorator for `DevToolsTarget` background tasks to manage their lifecycle.
    *   `TargetFilter(dataclass)`: Dataclass to define a filter for discovering new browser targets.
    *   `TargetData(dataclass)`: Dataclass to hold essential information about a browser target.
*   `logger.py`:
    *   `LoggerSettings(dataclass)`: Settings for configuring the LoggerManager.
    *   `LogEntry(dataclass)`: Represents a single log entry with detailed information.
    *   `TargetLogger`: Manages logging for a specific browser target.
    *   `build_target_logger(...)`: Builds and initializes a `TargetLogger` instance.
    *   `LogLevelStats(dataclass)`: Stores statistics for a specific log level.
    *   `LoggerChannelStats(dataclass)`: Stores statistics for a specific logging channel (per target).
    *   `TargetTypeStats(dataclass)`: Stores statistics for a specific target type.
    *   `MainLogEntry(dataclass)`: Represents a summary log entry for the entire logging system.
    *   `MainLogger`: Manages the main log file, summarizing overall logging activity.
    *   `build_main_logger(...)`: Builds and initializes a `MainLogger` instance.
*   `manager.py`:
    *   `DevToolsSettings(dataclass)`: Settings for configuring the DevTools manager.
    *   `DevToolsTarget`: Manages the DevTools Protocol session and event handling for a specific browser target.
    *   `DevTools`: Base class for handling DevTools functionalities in Selenium WebDriver.
*   `domains/`:
    *   `abstract.py`: Defines abstract base classes and TypedDicts for domain settings and handlers.
    *   `__init__.py`:
        *   `Domains(TypedDict)`: Settings for configuring callbacks for different DevTools event domains.
        *   `DomainsSettings(dataclass)`: Container for configuration settings across different DevTools domains.
        *   `domains_type`: Literal type for available domains (e.g., "fetch").
        *   `domains_classes_type`: Union type for domain configuration classes.
    *   `fetch.py`: Defines settings and handlers specific to the `Fetch` domain.
*   `domains_default/`:
    *   `fetch.py`: Defines default ready-to-use handlers to the `Fetch` domain.

## Future Notes

*   **Expanded Browser Support**: Implementations for other browsers like Firefox and Safari.
*   **Advanced Human-like Behaviors**: Further refinement of human-like interaction algorithms, potentially incorporating machine learning for more realistic user simulation (e.g., typing errors, variable delays based on content).
*   **Enhanced Proxy Management**: More flexible and robust proxy configuration, including support for proxy authentication and rotating proxies.
*   **More CDP Domain Implementations**: Expand support for other critical CDP domains like `Network`, `Page`, `DOM`, `Runtime`, `Security`, etc., with structured settings and handlers.
*   **Performance Monitoring Integration**: Provide built-in tools or examples for collecting and analyzing browser performance metrics via CDP.
*   **Screenshot and Video Capture**: Leverage CDP to enable advanced screenshot capabilities (e.g., full-page screenshots) and video recording of browser sessions.
*   **Customizable Logging Output**: Allow users to define custom log formats and output destinations beyond simple file writing.
*   **Interactive Debugging**: Explore possibilities for integrating with external debuggers or providing a basic interactive shell for CDP commands.
*   **Configuration Management**: Centralized and more declarative ways to manage browser configurations, possibly through YAML or TOML files.
*   **Cloud Selenium Grid Integration**: Direct integration with cloud-based Selenium grid providers (e.g., BrowserStack, Sauce Labs) for scalable testing.
*   **Browser Profile Management**: Add capabilities to locate and manage browser user profiles.
*   **WebDriver Manager Integration**: Potentially integrate with or provide utilities for automatic downloading and management of WebDriver executables to match installed browser versions.