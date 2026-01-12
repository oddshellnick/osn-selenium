# osn-selenium: Advanced Selenium wrapper with Trio support and CDP integration

osn-selenium is a comprehensive Python library that extends standard Selenium WebDriver capabilities by offering both synchronous and asynchronous (Trio-based) execution modes. It provides robust tools for managing browser flags via Pydantic models, advanced Chrome DevTools Protocol (CDP) interaction for network interception and event handling, and human-like input simulation to mimic natural user behavior.

## Technologies

| Name       | Badge                                                                                                                                                | Description                                                                                                                                            |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python     | [![Python](https://img.shields.io/badge/Python%2DPython?style=flat&logo=python&color=%231f4361)](https://www.python.org/)                            | The core programming language used to build the library.                                                                                               |
| Selenium   | [![Selenium](https://img.shields.io/badge/Selenium%2DSelenium?style=flat&logo=selenium&color=%23408631)](https://www.selenium.dev/)                  | The underlying browser automation framework that this library extends.                                                                                 |
| Trio       | [![Trio](https://img.shields.io/badge/Trio%2DTrio?style=flat&color=%23d2e7fa)](https://trio.readthedocs.io/)                                         | Used to provide an asynchronous, non-blocking interface for all WebDriver operations.                                                                  |
| Pydantic   | [![Pydantic](https://img.shields.io/badge/Pydantic%2DPydantic?style=flat&logo=pydantic&color=%23e92063)](https://docs.pydantic.dev/)                 | Used for data validation and managing complex configuration settings, especially for DevTools and browser flags.                                       |
| Pandas     | [![Pandas](https://img.shields.io/badge/Pandas%2DPandas?style=flat&logo=pandas&color=%23130654)](https://pandas.pydata.org/)                         | Utilized internally to process system process and network connection data for managing browser instances.                                              |
| PyWin32    | [![PyWin32](https://img.shields.io/badge/PyWin32%2DPyWin32?style=flat&color=%23e09716)](https://pypi.org/project/pywin32/)                           | Employed for Windows-specific functionalities, such as discovering installed browsers and retrieving their versions from the registry and executables. |
| Subprocess | [![Subprocess](https://img.shields.io/badge/subprocess%2Dsubprocess?style=flat&color=%23a3c910)](https://docs.python.org/3/library/subprocess.html)  | Used to execute the underlying system shell commands.                                                                                                  |

## Key Features

*   **Dual Execution Modes:**
    *   **Sync:** Standard blocking execution similar to vanilla Selenium but with enhanced features.
    *   **Trio Threads:** Fully asynchronous wrapper using Trio, allowing concurrent browser management and non-blocking background tasks.
*   **Advanced CDP Integration:**
    *   Direct access to Chrome DevTools Protocol commands.
    *   Event listeners for network activity (Fetch/Network domains) and target lifecycle events.
    *   Request interception and modification (continue, fail, or fulfill requests).
    *   Dedicated logging system for DevTools events with filtering capabilities.
*   **Typed Flag Management:**
    *   Pydantic-based configuration for Chrome, Edge, and Yandex browsers.
    *   Easy toggles for headless mode, user agents, proxy settings, and specific Blink engine features.
*   **Human-Like Interactions:**
    *   `HumanLikeActionChains` implementation.
    *   Simulates non-linear, curved mouse movements (Bezier-like).
    *   Variable typing speeds and smooth scrolling patterns to reduce bot detection.
*   **Browser Management:**
    *   Auto-detection of browser executables on Windows and Linux.
    *   Management of browser lifecycle, including port finding and clean process termination.

## Installation

1. Install library:
    *   **With pip:**
        ```bash
        pip install osn-selenium
        ```

        **With pip (beta versions):**
        ```bash
        pip install -i https://test.pypi.org/simple/ osn-selenium
        ```

    *   **With git:**
        ```bash
        pip install git+https://github.com/oddshellnick/osn-selenium.git
        ```
        *(Ensure you have git installed)*

2. **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Here are some examples of how to use `osn-selenium`:

### Synchronous Chrome Driver with Typed Flags

This example demonstrates standard usage with the added benefit of typed flag management.

```python
from osn_selenium.webdrivers.sync.chrome import ChromeWebDriver
from osn_selenium.flags.models.chrome import ChromeFlags, ChromeArguments

# Configure typed flags
flags = ChromeFlags(
    argument=ChromeArguments(
        headless_mode=False,
        mute_audio=True,
    )
)

# Initialize driver with auto-detected binary
driver = ChromeWebDriver(
    webdriver_path="path/to/chromedriver.exe",
    flags=flags
)

try:
    driver.start_webdriver()
    driver.get("https://www.google.com")
    print(driver.title())
    
    # Use Human-like actions
    element = driver.find_element(by="name", value="q")
    actions = driver.hm_action_chain()
    actions.hm_move_to_element(element)
    actions.click()
    actions.hm_text_input("Selenium")
    actions.perform()
finally:
    driver.close_webdriver()
```

### Asynchronous (Trio) with CDP Interception

This example shows how to use the Trio-based driver to intercept network requests via CDP.

```python
import trio
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.dev_tools.domains import DomainsSettings
from osn_selenium.dev_tools.domains.fetch import FetchSettings, FetchEnableKwargsSettings

async def main():
    # Configure DevTools to intercept all requests
    dt_settings = DevToolsSettings(
        domains_settings=DomainsSettings(
            fetch=FetchSettings(
                enable_func_kwargs=FetchEnableKwargsSettings(patterns=[{"urlPattern": "*"}])
            )
        )
    )

    driver = ChromeWebDriver(
        webdriver_path="path/to/chromedriver.exe",
        devtools_settings=dt_settings
    )

    await driver.start_webdriver()

    # Context manager activates DevTools listeners and establishes BiDi connection
    async with driver.dev_tools:
        await driver.get("https://www.example.com")
        # Interception logic is handled in background tasks managed by the DevTools nursery
        await trio.sleep(5)

    await driver.close_webdriver()

trio.run(main)
```

## Classes and Functions

### WebDrivers (`osn_selenium.webdrivers`)

Contains the main entry points for browser automation, separated into synchronous and asynchronous implementations.

#### Sync Implementation (`osn_selenium.webdrivers.sync`)
*   `chrome.ChromeWebDriver`
    *   Specific implementation for Google Chrome. Inherits all capabilities from `CoreWebDriver`.
*   `edge.EdgeWebDriver`
    *   Specific implementation for Microsoft Edge.
*   `yandex.YandexWebDriver`
    *   Specific implementation for Yandex Browser.
*   `core.CoreWebDriver`
    *   Base class aggregating all mixins (Actions, Capture, Elements, Navigation, etc.).

#### Trio/Async Implementation (`osn_selenium.webdrivers.trio_threads`)
*   `chrome.ChromeWebDriver`
    *   Asynchronous implementation for Google Chrome. All methods are awaitable.
*   `edge.EdgeWebDriver`
    *   Asynchronous implementation for Microsoft Edge.
*   `yandex.YandexWebDriver`
    *   Asynchronous implementation for Yandex Browser.

### Flag Management (`osn_selenium.flags`)

Provides typed models for configuring browser startup arguments and preferences.

*   `models.chrome.ChromeFlags`
    *   Comprehensive model aggregating arguments, experimental options, and attributes for Chrome.
*   `models.blink.BlinkArguments`
    *   Typed model for common command-line arguments (e.g., `headless_mode`, `user_agent`, `proxy_server`).
*   `base.BrowserFlagsManager`
    *   `set_flags(...)`: Clears and sets new flags based on the provided model.
    *   `update_flags(...)`: Updates existing flags without clearing.
    *   `options`: Property that returns the Selenium Options object ready for the driver.

### DevTools Protocol (`osn_selenium.dev_tools`)

Manages the connection to the Chrome DevTools Protocol (CDP) for advanced control.

*   `manager.DevTools`
    *   The main manager class used as an async context manager. Handles WebSocket connections and nurseries.
*   `settings.DevToolsSettings`
    *   Configuration for the DevTools manager, including log settings and target filters.
*   `target.DevToolsTarget`
    *   Represents a specific browser target (page, iframe, worker).
    *   `log(...)`: Logs messages specific to this target.
*   `domains.fetch.FetchSettings`
    *   Configures the `Fetch` domain for network interception.

### Instances & Interaction (`osn_selenium.instances`)

Wrappers around standard Selenium objects to support extended functionality and type safety.

#### Synchronous Instances (`osn_selenium.instances.sync`)
*   `action_chains.HumanLikeActionChains`
    *   `hm_move(...)`: Moves the mouse cursor in a human-like curve to coordinates.
    *   `hm_move_to_element(...)`: Moves the mouse to an element naturally.
    *   `hm_text_input(...)`: Types text with variable human-like delays.
    *   `hm_scroll_to_element(...)`: Smoothly scrolls to an element.
*   `web_element.WebElement`
    *   Wrapper for Selenium's WebElement with additional utility methods.
    *   `screenshot_as_png(...)`: Returns the element screenshot as bytes.

#### Trio Instances (`osn_selenium.instances.trio_threads`)
*   `action_chains.HumanLikeActionChains`
    *   Asynchronous version of the human-like action chains.
    *   `hm_move(...)`: Awaitable human-like move.
*   `web_element.WebElement`
    *   Asynchronous wrapper for WebElement.
    *   `click(...)`: Awaitable click action.
    *   `send_keys(...)`: Awaitable key input.

### Executors (`osn_selenium.executors`)

Handles low-level execution of commands.

*   `javascript.JSExecutor`
    *   `check_element_in_viewport(...)`: Checks if an element is visible in the current viewport via JS.
    *   `get_element_rect_in_viewport(...)`: Returns the bounding box relative to the viewport.
    *   `stop_window_loading(...)`: Stops the page loading process.
*   `cdp.CDPExecutor`
    *   Provides typed methods for all CDP domains (Network, Page, DOM, etc.).
    *   `execute(...)`: Executes a raw CDP command.

## Notes

*   **Concurrency Constraints in `trio_threads`:** 
    The `trio_threads` implementation is built using a unified `trio.Lock`. This means that every driver function and every associated instance (including `ActionChains`, `WebElement`, `Alert`, etc.) can execute only one operation at a time. Do not attempt to parallelize multiple operations (coroutines) within a single browser instance, as they will be queued sequentially. The primary purpose of this asynchronous implementation is to enable the simultaneous management of **multiple browser instances** within a single event loop, rather than concurrent interactions with one browser.
*   **CDP Domains and Background Tasks:** 
    When configuring the domains for network interception, it is highly recommended to provide a `target_background_task` in your `DevToolsSettings`. This is especially critical for websites that dynamically create numerous targets (such as iframes or workers). Without a proper background task to handle these events, the browser's execution flow might hang or fail to process requests for nested targets properly.

## Future Notes

*   **Advanced Fingerprinting Update:** A major global update is in development to include a sophisticated **browser fingerprinting suite**. This will enable spoofing of hardware-based identifiers (Canvas, WebGL, WebAudio, etc.) to significantly enhance evasion of advanced anti-bot systems.
*   **Firefox (GeckoDriver) Support:** Implementation of Gecko-specific flags and full BiDi/CDP integration for Firefox.
*   **macOS Support:** Extending browser auto-detection and lifecycle management for macOS environments.
*   **High-Level CDP Handlers:** Expanding the `dev_tools.domains` module to include simplified event-driven logic for `Network`, `Page`, and `Runtime` domains, similar to the current `Fetch` implementation.
*   **Enhanced Human-Like Actions:** Adding more complex Bezier-based mouse movement patterns and advanced typing jitter to further decrease automation footprints.