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
    *   **Sync:** Enhanced synchronous WebDrivers compatible with standard Selenium usage.
    *   **Trio Threads:** Fully asynchronous WebDrivers using Trio, enabling non-blocking operations and concurrent browser management.
*   **Advanced CDP Integration:**
    *   Direct access to Chrome DevTools Protocol commands via `driver.cdp`.
    *   Dedicated `DevTools` manager for event listening (e.g., `Fetch`, `Network` domains).
    *   Support for request interception, modification, and authentication handling.
*   **Typed Flag Management:**
    *   Pydantic-based configuration for Chrome, Edge, and Yandex browsers.
    *   Structured access to arguments, experimental options, and attributes.
*   **Human-Like Interactions:**
    *   `HumanLikeActionChains` for natural mouse movements (Bezier-like curves).
    *   Variable typing speeds and randomized scrolling patterns.
*   **Browser Lifecycle Management:**
    *   Auto-detection of browser binaries on Windows and Linux.
    *   Smart port finding and process cleanup.
*   **Fingerprint Detection:**
    *   Built-in scripts and logging to detect if the target website is probing browser fingerprints.

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

```python
from osn_selenium.webdrivers.sync.chrome import ChromeWebDriver
from osn_selenium.flags.models.chrome import ChromeFlags, ChromeArguments

# Configure typed flags using Pydantic models
flags = ChromeFlags(
    argument=ChromeArguments(
        headless_mode=False,
        mute_audio=True,
        no_first_run=True
    )
)

# Initialize driver (auto-detects binary)
driver = ChromeWebDriver(
    webdriver_path="path/to/chromedriver.exe",
    flags=flags
)

try:
    driver.start_webdriver()
    driver.get("https://www.google.com")
    
    # Use Human-like actions
    search_box = driver.find_element(by="name", value="q")
    actions = driver.hm_action_chain()
    actions.hm_move_to_element(search_box)
    actions.click()
    actions.hm_text_input("Selenium automation") # Types with variable delay
    actions.perform()
    
finally:
    driver.close_webdriver()
```

### Asynchronous (Trio) with CDP Interception

```python
import trio
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.dev_tools.domains import DomainsSettings
from osn_selenium.dev_tools.domains.fetch import FetchSettings, FetchEnableKwargsSettings

async def main():
    # Configure DevTools to intercept specific requests
    dt_settings = DevToolsSettings(
        domains_settings=DomainsSettings(
            fetch=FetchSettings(
                enable_func_kwargs=FetchEnableKwargsSettings(
                    patterns=[{"urlPattern": "*api*", "requestStage": "Request"}]
                )
            )
        )
    )

    driver = ChromeWebDriver(
        webdriver_path="path/to/chromedriver.exe",
        devtools_settings=dt_settings
    )

    await driver.start_webdriver()

    # Async context manager starts CDP listeners
    async with driver.devtools:
        await driver.get("https://example.com")
        # Logic for handling intercepted requests runs in background tasks
        await trio.sleep(5)

    await driver.close_webdriver()

trio.run(main)
```

## Classes and Functions

### WebDrivers (`osn_selenium.webdrivers`)

This package contains the main entry points for browser automation, split into synchronous and asynchronous implementations.

#### Sync (`osn_selenium.webdrivers.sync`)
*   `chrome.ChromeWebDriver` - Implementation for Google Chrome with synchronous methods.
*   `edge.EdgeWebDriver` - Implementation for Microsoft Edge with synchronous methods.
*   `yandex.YandexWebDriver` - Implementation for Yandex Browser with synchronous methods.
*   `core.CoreWebDriver` - The base class aggregating all mixins (Actions, Capture, Navigation, etc.).

#### Trio (`osn_selenium.webdrivers.trio_threads`)
*   `chrome.ChromeWebDriver` - Asynchronous implementation for Google Chrome. All interaction methods are awaitable.
*   `edge.EdgeWebDriver` - Asynchronous implementation for Microsoft Edge.
*   `yandex.YandexWebDriver` - Asynchronous implementation for Yandex Browser.

### Flags Management (`osn_selenium.flags`)

Provides Pydantic models for type-safe browser configuration.

*   `models.chrome.ChromeFlags` - Comprehensive model for Chrome (arguments, experimental options, attributes).
*   `models.blink.BlinkArguments` - Typed model for common Blink-engine arguments (e.g., `headless_mode`, `user_agent`, `proxy_server`).
*   `models.blink.BlinkFeatures` - Typed model for specific Blink features (e.g., `automation_controlled`).
*   `base.BrowserFlagsManager` - Manages the application of flags to the WebDriver options instance.

### DevTools Protocol (`osn_selenium.dev_tools`)

Manages the connection and interaction with the Chrome DevTools Protocol.

*   `manager.DevTools` - The main coordinator for CDP sessions, handling WebSocket connections and Trio nurseries.
*   `target.DevToolsTarget` - Represents a specific browser target (page, iframe, worker) with its own CDP session.
*   `settings.DevToolsSettings` - Configuration for the manager, including logging paths and target filters.
*   `domains.fetch.FetchSettings` - Configuration for the Fetch domain to intercept/modify network requests.

### Instances & Interaction (`osn_selenium.instances`)

Wrappers around standard Selenium objects providing additional functionality and `trio` compatibility.

*   `web_element.WebElement` - Wrapper for `selenium.webdriver.remote.webelement.WebElement`.
*   `action_chains.ActionChains` - Wrapper for `selenium.webdriver.common.action_chains.ActionChains`.
*   `action_chains.HumanLikeActionChains` - Extends `ActionChains` with:
    *   `hm_move(...)` - Moves mouse in a realistic curve.
    *   `hm_text_input(...)` - Types text with realistic delays.
    *   `hm_scroll_to_element(...)` - Smooth scrolling logic.
*   `alert.Alert` - Wrapper for handling alerts.
*   `shadow_root.ShadowRoot` - Wrapper for Shadow DOM roots.

### Executors (`osn_selenium.executors`)

Backend logic for executing commands.

*   `javascript.JSExecutor` - Helper for executing common JS snippets (e.g., `check_element_in_viewport`, `get_document_scroll_size`).
*   `cdp.CDPExecutor` - Provides typed methods for all CDP domains (Network, Page, DOM, Input, etc.).

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