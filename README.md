# osn-selenium: Advanced Selenium wrapper with Trio support and CDP integration

osn-selenium is a comprehensive Python library that extends standard Selenium WebDriver capabilities by offering both synchronous and asynchronous (Trio-based) execution modes. It provides robust tools for managing browser flags via Pydantic models, advanced Chrome DevTools Protocol (CDP) interaction for network interception and event handling, and human-like input simulation to mimic natural user behavior.

## Technologies

| Name     | Badge                                                                                                                                | Description                                                                                                                                            |
|----------|--------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python   | [![Python](https://img.shields.io/badge/Python%2DPython?style=flat&logo=python&color=%231f4361)](https://www.python.org/)            | The core programming language used to build the library.                                                                                               |
| Selenium | [![Selenium](https://img.shields.io/badge/Selenium%2DSelenium?style=flat&logo=selenium&color=%23408631)](https://www.selenium.dev/)  | The underlying browser automation framework that this library extends.                                                                                 |
| Trio     | [![Trio](https://img.shields.io/badge/Trio%2DTrio?style=flat&color=%23d2e7fa)](https://trio.readthedocs.io/)                         | Used to provide an asynchronous, non-blocking interface for all WebDriver operations.                                                                  |
| Pydantic | [![Pydantic](https://img.shields.io/badge/Pydantic%2DPydantic?style=flat&logo=pydantic&color=%23e92063)](https://docs.pydantic.dev/) | Used for data validation and managing complex configuration settings, especially for DevTools and browser flags.                                       |
| Pandas   | [![Pandas](https://img.shields.io/badge/Pandas%2DPandas?style=flat&logo=pandas&color=%23130654)](https://pandas.pydata.org/)         | Utilized internally to process system process and network connection data for managing browser instances.                                              |
| PyWin32  | [![PyWin32](https://img.shields.io/badge/PyWin32%2DPyWin32?style=flat&color=%23e09716)](https://pypi.org/project/pywin32/)           | Employed for Windows-specific functionalities, such as discovering installed browsers and retrieving their versions from the registry and executables. |

## Key Features

*   **Dual Execution Modes:**
    *   **Sync:** Standard blocking execution similar to vanilla Selenium.
    *   **Trio Threads:** Fully asynchronous wrapper using Trio, allowing concurrent browser management and non-blocking background tasks.
*   **Advanced CDP Integration:**
    *   Direct access to Chrome DevTools Protocol commands.
    *   Event listeners for network activity (Fetch/Network domains).
    *   Request interception and modification (continue, fail, or fulfill requests).
    *   Dedicated logging system for DevTools events.
*   **Browser Flag Management:**
    *   Typed configuration for Chrome, Edge, and Yandex browsers.
    *   Easy toggle for headless mode, user agents, proxy settings, and Blink-specific features.
*   **Human-Like Interactions:**
    *   `HumanLikeActionChains` implementation.
    *   Simulates non-linear, curved mouse movements.
    *   Variable typing speeds and scrolling patterns to reduce bot detection.
*   **Browser Management:**
    *   Auto-detection of browser executables on Windows.
    *   Management of browser lifecycle, including port finding and process termination.

## Installation

1.  **Install library:**
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

2.  **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```

    *Note: This library currently relies on `osn-windows-cmd`, making it Windows-specific.*

## Usage

Here are some examples of how to use `osn-selenium`:

### Synchronous Chrome Driver

This example demonstrates standard usage with the added benefit of typed flag management.

```python
from osn_selenium.webdrivers.sync.chrome import ChromeWebDriver
from osn_selenium.flags.models.chrome import ChromeFlags, ChromeArguments

# Configure flags
flags = ChromeFlags(
    argument=ChromeArguments(
        headless_mode=False,
        mute_audio=True,
    )
)

# Initialize driver
driver = ChromeWebDriver(
    webdriver_path="path/to/chromedriver.exe",
    flags=flags
)

try:
    driver.start_webdriver()
    driver.get("https://www.google.com")
    print(driver.title())
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
    # Configure DevTools to intercept requests
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

    # Context manager activates DevTools listeners
    async with driver.dev_tools:
        await driver.get("https://www.example.com")
        # Logic to handle intercepted requests happens in background tasks
        await trio.sleep(5)

    await driver.close_webdriver()

trio.run(main,)
```

## Classes and Functions

### WebDrivers (`osn_selenium.webdrivers`)
This module contains the main entry points for browser automation, separated into synchronous and asynchronous implementations.

*   `sync` (Package)
    *   `base.WebDriver`: The base synchronous WebDriver class implementing standard Selenium methods.
    *   `blink.BlinkWebDriver`: Base driver for Blink-based browsers (Chrome, Edge), handling executable detection and debugging ports.
    *   `chrome.ChromeWebDriver`: Specific implementation for Google Chrome.
    *   `edge.EdgeWebDriver`: Specific implementation for Microsoft Edge.
    *   `yandex.YandexWebDriver`: Specific implementation for Yandex Browser.
*   `trio_threads` (Package)
    *   `base.WebDriver`: The asynchronous WebDriver class using Trio for concurrency. Methods are awaitable (e.g., `await driver.get()`).
    *   `chrome.ChromeWebDriver`: Async implementation for Google Chrome.
    *   `edge.EdgeWebDriver`: Async implementation for Microsoft Edge.

### Flag Management (`osn_selenium.flags`)
Provides typed models for configuring browser startup arguments and preferences.

*   `base.BrowserFlagsManager`: Manages the construction of command-line arguments and capabilities.
*   `models.base.BrowserFlags`: Pydantic model aggregating arguments, experimental options, and attributes.
*   `models.chrome.ChromeFlags`: Specific flags for Chrome, including `ChromeArguments` (e.g., `headless_mode`, `user_agent`).
*   `models.blink.BlinkFeatures`: Configuration for internal Blink engine features.

### DevTools Protocol (`osn_selenium.dev_tools`)
Manages the connection to the Chrome DevTools Protocol.

*   `manager.DevTools`: The main manager class used as a context manager (`async with driver.dev_tools`). It handles the WebSocket connection and event loop.
*   `target.DevToolsTarget`: Represents a specific browser target (page, iframe) being monitored.
*   `settings.DevToolsSettings`: Configuration for the DevTools manager, including filters for new targets.
*   `domains.fetch.FetchSettings`: Configures the `Fetch` domain for network interception.

### Instances & Interaction (`osn_selenium.instances`)
Wrappers around standard Selenium objects to support extended functionality.

*   `sync.action_chains.HumanLikeActionChains`: Extends Selenium's ActionChains.
    *   `hm_move(start, end)`: Moves mouse in a human-like curve.
    *   `hm_text_input(text)`: Types text with variable delays.
*   `sync.web_element.WebElement`: Wrapper for `selenium.webdriver.remote.webelement.WebElement`, ensuring type compatibility with the library's internal logic.
*   `trio_threads.web_element.WebElement`: Async version of the WebElement wrapper.

### Executors (`osn_selenium.executors`)
Handles low-level execution of commands.

*   `javascript.AbstractJSExecutor`: Interface for executing JavaScript.
    *   `check_element_in_viewport(element)`: Checks if an element is visible in the current viewport.
    *   `get_element_rect_in_viewport(element)`: Returns the bounding box relative to the viewport.
*   `cdp.AbstractCDPExecutor`: Interface for executing raw CDP commands.

## Notes

*   **Concurrency Constraints in `trio_threads`:** 
    The `trio_threads` implementation is built using a unified `trio.Lock`. This means that every driver function and every associated instance (including `ActionChains`, `WebElement`, `Alert`, etc.) can execute only one operation at a time. Do not attempt to parallelize multiple operations (coroutines) within a single browser instance, as they will be queued sequentially. The primary purpose of this asynchronous implementation is to enable the simultaneous management of **multiple browser instances** within a single event loop, rather than concurrent interactions with one browser.
*   **CDP Fetch Domain and Background Tasks:** 
    When configuring the `Fetch` domain for network interception, it is highly recommended to provide a `target_background_task` in your `DevToolsSettings`. This is especially critical for websites that dynamically create numerous targets (such as iframes or workers). Without a proper background task to handle these events, the browser's execution flow might hang or fail to process requests for nested targets properly.

## Future Notes

*   **Cross-Platform Support:** Currently, the process management logic is heavily tied to Windows (`osn-windows-cmd`). Future updates aim to abstract this for Linux and macOS support.
*   **Firefox Support:** While the architecture supports it abstractly, concrete implementations for Firefox (GeckoDriver) flags and DevTools integration are planned.
*   **Enhanced Human-Like Actions:** More complex patterns for mouse movement and interaction behaviors to further reduce bot detection vectors.
*   **Expanded CDP Domains:** Full support for additional CDP domains like `Network`, `Page`, and `Runtime` beyond the current `Fetch` focus.