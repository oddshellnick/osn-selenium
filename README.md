# osn-selenium: Advanced Selenium Wrapper with Async Support and Fingerprinting Protection

osn-selenium is a robust wrapper around Selenium WebDriver designed for automation of Blink-based browsers (Chrome, Edge, Yandex). It extends standard Selenium capabilities by providing native asynchronous support via Trio, deep integration with the Chrome DevTools Protocol (CDP), sophisticated browser fingerprint spoofing, and human-like user interaction simulation.

For more detailed information, please visit the [wiki page](https://github.com/oddshellnick/osn-selenium/wiki).

## Technologies

| Name       | Badge                                                                                                                                               | Description                                                                                                                                            |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python     | [![Python](https://img.shields.io/badge/Python%2DPython?style=flat&logo=python&color=%231f4361)](https://www.python.org/)                           | The core programming language used to build the library.                                                                                               |
| JavaScript | [![JavaScript](https://img.shields.io/badge/JavaScript%2DJavaScript?style=flat&logo=javascript&color=%23998805)](https://developer.mozilla.org/)    | Used for browser-side logic injection, complex fingerprint spoofing, and advanced geometry/viewport calculations.                                      |
| Selenium   | [![Selenium](https://img.shields.io/badge/Selenium%2DSelenium?style=flat&logo=selenium&color=%23408631)](https://www.selenium.dev/)                 | The underlying browser automation framework that this library extends.                                                                                 |
| Trio       | [![Trio](https://img.shields.io/badge/Trio%2DTrio?style=flat&color=%23d2e7fa)](https://trio.readthedocs.io/)                                        | Used to provide an asynchronous, non-blocking interface for all WebDriver operations.                                                                  |
| Pydantic   | [![Pydantic](https://img.shields.io/badge/Pydantic%2DPydantic?style=flat&logo=pydantic&color=%23e92063)](https://docs.pydantic.dev/)                | Used for data validation and managing complex configuration settings, especially for DevTools and browser flags.                                       |
| psutil     | [![psutil](https://img.shields.io/badge/psutil%2Dpsutil?style=flat&color=%230f90a1)](https://pypi.org/project/psutil/)                              | Used for robust process management and network connection tracking across different operating systems.                                                 |
| PyWin32    | [![PyWin32](https://img.shields.io/badge/PyWin32%2DPyWin32?style=flat&color=%23e09716)](https://pypi.org/project/pywin32/)                          | Employed for Windows-specific functionalities, such as discovering installed browsers and retrieving their versions from the registry and executables. |
| Subprocess | [![Subprocess](https://img.shields.io/badge/subprocess%2Dsubprocess?style=flat&color=%23a3c910)](https://docs.python.org/3/library/subprocess.html) | Used to execute the underlying system shell commands.                                                                                                  |

## Key Features

*   **Dual Operation Modes:**
    *   **Synchronous:** Standard blocking execution similar to vanilla Selenium.
    *   **Asynchronous (Trio):** Fully async implementation allowing concurrent control of browser targets using the Trio library.
*   **Deep CDP Integration:**
    *   Direct access to Chrome DevTools Protocol domains (Network, Page, DOM, Security, etc.).
    *   Event listening and handling (e.g., intercepting network requests, console logs).
*   **Advanced Fingerprint Spoofing:**
    *   `FingerprintSettings` module to inject scripts detecting and modifying browser fingerprints.
    *   Spoofing capabilities for Canvas, WebGL, AudioContext, Fonts, Screen properties, and more.
    *   Configurable noise generation (static or random) to evade anti-bot detection.
*   **Human-Like Interactions:**
    *   `HumanLikeActionChains` simulating natural mouse movements (Bezier curves, deviations) and typing speeds.
    *   Smooth scrolling algorithms.
*   **Browser Lifecycle Management:**
    *   Auto-detection of installed browsers (Chrome, Edge, Yandex).
    *   Robust handling of browser processes, including zombie process cleanup and port management.
    *   Structured management of browser flags, arguments, and experimental options.
*   **Enhanced Element Interaction:**
    *   Wrappers for WebElements, ShadowRoots, and Alerts with additional utility methods.
    *   Built-in JavaScript execution helpers for viewport checks and geometry retrieval.

## Installation

1.  **Install library:**

    *   **With pip:**
        ```bash
        pip install osn-selenium
        ```

        **With pip (beta versions):**
        ```bash
        pip install -i https://test.pypi.org/simple/ osn_system_utils
        ```

    *   **With git:**
        ```bash
        pip install git+https://github.com/oddshellnick/osn-selenium.git
        ```
        *(Ensure you have git installed)*

    *   **With git (beta versions):**
        ```bash
        pip install git+https://github.com/oddshellnick/osn-selenium.git@dev
        ```
        *(Ensure you have git installed)*

2.  **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Here are some examples of how to use `osn-selenium`:

### Synchronous Chrome with Human-Like Actions

```python
from osn_selenium.webdrivers.sync.chrome import ChromeWebDriver
from osn_selenium.models import WindowRect
# Initialize driver with specific window size
driver = ChromeWebDriver(
		webdriver_path="webdriver.exe",
		window_rect=WindowRect(width=1280, height=720)
)

try:
	driver.start_webdriver()
	driver.get("https://google.com")

	# Locate search bar
	search_bar = driver.find_element(by="name", value="q")

	# Use HumanLikeActionChains for natural typing
	actions = driver.action_chains()
	actions.hm_move_to_element(search_bar)
	actions.click()
	actions.hm_text_input("Selenium automation")
	actions.perform()
finally:
	driver.quit()
```

### Asynchronous (Trio) with Fingerprint Spoofing

```python
import trio
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.javascript.fingerprint import FingerprintSettings

async def main():
    # Configure fingerprint spoofing
    fp_settings = FingerprintSettings(
        optimize_events=True,
        # Detect and spoof specific APIs
        use_preset_registry=True
    )
    
    # Configure DevTools
    dt_settings = DevToolsSettings(
        fingerprint_settings=fp_settings
    )

    driver = ChromeWebDriver(
        webdriver_path="webdriver.exe",
        devtools_settings=dt_settings
    )

    try:
        await driver.start_webdriver()
        
        # Start DevTools session to inject spoofing scripts
        async with driver.devtools:
            await driver.get("https://browserleaks.com/canvas")
            await trio.sleep(10) # Let the page load and scripts run
    finally:
        await driver.quit()

trio.run(main)
```

## Classes and Functions

### WebDrivers (`osn_selenium.webdrivers`)

This package contains the main entry points for initializing browser automation. It is split into `sync` and `trio_threads` subpackages.

*   `CoreWebDriver`
    *   Base class aggregating all mixins (Actions, Auth, Capture, CDP, Elements, File, Lifecycle, Navigation, Script, Settings, Storage, Timeouts, Window).
*   `ChromeWebDriver` (Available in `sync` and `trio_threads`)
    *   `__init__(...)`: Initializes the Chrome driver with paths, flags managers, and timeout settings.
    *   `start_webdriver(...)`: Starts the browser process and the WebDriver session.
    *   `quit()`: Closes the browser and session.
*   `EdgeWebDriver` (Available in `sync` and `trio_threads`)
    *   Specialized WebDriver for Microsoft Edge.
*   `YandexWebDriver` (Available in `sync` and `trio_threads`)
    *   Specialized WebDriver for Yandex Browser.

### Browser Flags (`osn_selenium.flags`)

Manages configuration for browser launch arguments and capabilities.

*   `BrowserFlagsManager`
    *   `set_argument(argument, value)`: Sets a command-line argument.
    *   `set_experimental_option(option, value)`: Sets a WebDriver experimental option.
    *   `build_options_arguments(options)`: Applies arguments to the Selenium Options object.
*   `ChromeFlagsManager` / `EdgeFlagsManager` / `YandexFlagsManager`
    *   Subclasses with specific default flags and binary detection logic for their respective browsers.

### DevTools Protocol (`osn_selenium.dev_tools`)

Manages the connection to Chrome DevTools Protocol for low-level control.

*   `DevTools`
    *   `run()`: Initializes the BiDi connection and starts event listeners.
    *   `stop(...)`: Cleans up resources and closes connections.
*   `DevToolsTarget`
    *   Represents a specific target (tab/page) being controlled.
*   `CDPExecutor` (Available in `executors.sync.cdp` and `executors.trio_threads.cdp`)
    *   `execute(cmd, cmd_args)`: Sends a raw CDP command.
    *   `network`: Access to `Network` domain commands (cookies, cache, interception).
    *   `page`: Access to `Page` domain commands (navigation, printing, screenshots).
    *   `dom`: Access to `DOM` domain commands.
    *   `emulation`: Access to `Emulation` domain (device metrics, user agent, sensors).
    *   *(Includes accessors for all mapped CDP domains like Fetch, Storage, Runtime, etc.)*

### Instances Wrappers (`osn_selenium.instances`)

Wrappers around standard Selenium objects to provide enhanced functionality or async compatibility.

*   `WebElement`
    *   `click()`: Clicks the element.
    *   `send_keys(...)`: Types into the element.
    *   `screenshot(filename)`: Takes a screenshot of the specific element.
    *   `find_element(...)`: Finds a child element.
*   `ActionChains` / `HumanLikeActionChains`
    *   `hm_move_to_element(...)`: Moves mouse to element using human-like curves.
    *   `hm_text_input(...)`: Types text with random delays between keystrokes.
    *   `hm_scroll(...)`: Scrolls the page smoothly.
*   `ShadowRoot`
    *   `find_element(...)`: Finds elements inside a Shadow DOM.

### Javascript & Fingerprinting (`osn_selenium.javascript`)

Utilities for executing JS and managing browser fingerprints.

*   `FingerprintSettings`
    *   `generate_js()`: Creates the injection script for fingerprint spoofing based on the registry configuration.
*   `JSExecutor`
    *   `execute(script, ...)`: Executes raw JavaScript.
    *   `check_element_in_viewport(element)`: Returns True if element is visible in viewport.
    *   `get_element_rect_in_viewport(element)`: Returns element coordinates relative to viewport.

## Notes

*   **CDP Versioning and External Packages:** 
    This library supports a modular CDP (Chrome DevTools Protocol) architecture. Since standard Selenium distributions often deprecate or remove older protocol versions, we maintain a dedicated repository for all versions at [osn-selenium-cdp](https://github.com/oddshellnick/osn-selenium-cdp).
    *   **Manual Installation:** You can install specific CDP support by targeting the corresponding branch (e.g., `pip install git+https://github.com/oddshellnick/osn-selenium-cdp.git@v131`).
    *   **Structure Requirement:** If you choose to add or create CDP version packages manually, they **must strictly follow the directory structure** used in the `osn-selenium-cdp` repository. This ensures that the internal `MetaPathFinder` hook can correctly intercept and redirect imports from `selenium.webdriver.common.devtools`. Deviating from this structure will result in `CDPPackageError` or `ImportError`.
*   **Concurrency Constraints in `trio_threads`:** 
    The `trio_threads` implementation is built using a unified `trio.Lock`. This means that every driver function and every associated instance (including `ActionChains`, `WebElement`, `Alert`, etc.) can execute only one operation at a time. Do not attempt to parallelize multiple operations (coroutines) within a single browser instance, as they will be queued sequentially. The primary purpose of this asynchronous implementation is to enable the simultaneous management of **multiple browser instances** within a single event loop, rather than concurrent interactions with one browser.
*   **CDP Domains and Background Tasks:** 
    When configuring the domains for network interception, it is highly recommended to provide a `target_background_task` in your `DevToolsSettings`. This is especially critical for websites that dynamically create numerous targets (such as iframes or workers). Without a proper background task to handle these events, the browser's execution flow might hang or fail to process requests for nested targets properly.

## Future Notes

*   **Hybrid Composition Support:** We are preparing to expose all mixin-based functionality as distinct attributes within `CoreWebDriver` and `BlinkWebDriver` (e.g., `driver.navigation.get()`, `driver.storage.add_cookie()`). This will provide a cleaner, more modular alternative to the flat API while maintaining 100% backward compatibility with standard Selenium-like calls.
*   **Firefox (GeckoDriver) Support:** Implementation of Gecko-specific flags and full BiDi/CDP integration for Firefox.
*   **macOS Support:** Extending browser auto-detection and lifecycle management for macOS environments.
*   **High-Level CDP Handlers:** Expanding the `dev_tools.domains` module to include simplified event-driven logic for `Network`, `Page`, and `Runtime` domains, similar to the current `Fetch` implementation.
*   **Enhanced Human-Like Actions:** Adding more complex Bezier-based mouse movement patterns and advanced typing jitter to further decrease automation footprints.
*   **Single-Instance Internal Concurrency Research:** While the current `trio_threads` implementation is optimized for managing multiple browser instances concurrently, we are researching ways to enable parallel command execution within a *single* browser instance. This long-term goal involves moving away from the global `trio.Lock` toward a more granular task-dispatching system (potentially using `trio.MemorySendChannel` or direct CDP interaction) to allow simultaneous operations without protocol desynchronization.