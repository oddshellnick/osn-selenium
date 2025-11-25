# osn_selenium: An advanced, asynchronous wrapper for the Selenium library.

An advanced, asynchronous wrapper for Selenium designed for fine-grained browser control. It leverages `trio` for async operations, provides human-like action chains for more natural automation, and offers deep integration with the Chrome DevTools Protocol (CDP) for advanced features like network interception. The library is structured to be extensible, with built-in support for Blink-based browsers like Chrome, Edge, and Yandex, and includes utilities for managing browser flags and detecting installed browsers on the system.

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

*   **Asynchronous Interface**: Fully asynchronous API built on `trio` for high-performance, non-blocking browser automation.
*   **Multi-Browser Support**: Provides dedicated classes and flag managers for Blink-based browsers:
    *   Google Chrome
    *   Microsoft Edge
    *   Yandex Browser
*   **Human-Like Actions**: Includes `HumanLikeActionChains` to simulate natural user interactions:
    *   Curved mouse movements.
    *   Smooth, physics-based scrolling.
    *   Variable-delay text input to mimic human typing.
*   **Advanced DevTools Integration**:
    *   Deep control via Chrome DevTools Protocol (CDP) through an async context manager.
    *   Built-in support for the `Fetch` domain to intercept, modify, or block network requests and responses.
    *   Structured and extensible system for adding handlers for any CDP domain and event.
    *   Comprehensive logging for DevTools events on a per-target basis.
*   **Flexible Configuration**:
    *   A powerful `FlagsManager` system to granularly control browser startup arguments, experimental options, attributes, and Blink features.
    *   Pydantic-based settings for type-safe and clear configuration.
*   **System Integration & Management**:
    *   Utilities to automatically detect installed browsers and their versions on Windows.
    *   Manages browser processes and remote debugging ports, including finding free ports or reattaching to existing sessions.

## Installation

1.  Install library:
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

## Usage

Here are some examples of how to use `osn_selenium`:

### Basic Asynchronous WebDriver Usage

```python
import trio
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver

async def main():
    # Initialize the WebDriver
    # Replace 'path/to/chromedriver' with your actual path
    driver = ChromeWebDriver(webdriver_path='path/to/chromedriver')

    try:
        # Start the browser
        await driver.start_webdriver()

        # Navigate to a URL
        await driver.get("https://www.python.org")

        # Print the title
        title = await driver.title()
        print(f"Page title: {title}")

    finally:
        # Ensure the browser is closed
        await driver.close_webdriver()

if __name__ == "__main__":
    trio.run(main)
```

### Human-Like Mouse Movement

```python
import trio
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
from osn_selenium.webdrivers.types import Point

async def main():
    driver = ChromeWebDriver(webdriver_path='path/to/chromedriver')
    try:
        await driver.start_webdriver()
        await driver.get("https://github.com")

        # Find the search bar
        search_bar = await driver.find_element("css selector", '[data-target="qb-clone.input"]')

        # Create a human-like action chain
        actions = await driver.hm_action_chain()

        # Simulate moving the mouse from (0,0) to the search bar and clicking it
        start_point = Point(x=0, y=0)
        await actions.hm_move_to_element(start_point, search_bar)
        await actions.click()
        await actions.perform()
        
        # Simulate typing with human-like delays
        await (await driver.hm_action_chain()).hm_text_input("osn-selenium").perform()

        await trio.sleep(5) # Pause to observe

    finally:
        await driver.close_webdriver()

if __name__ == "__main__":
    trio.run(main)
```

## Classes and Functions

### Core Modules (`osn_selenium`)
*   `errors`: Contains custom exceptions.
    *   `PlatformNotSupportedError`: Raised when an operation is attempted on an unsupported OS.
*   `types`: Core Pydantic models for data structures.
    *   `DictModel`, `ExtraDictModel`: Base models for configuration.
    *   `Position`, `Size`, `Rectangle`, `WindowRect`: Geometric types.
*   `utils`:
    *   `JS_Scripts`: A model holding predefined JavaScript snippets.
*   `_functions`:
    *   `read_js_scripts()`: Reads JS files from the `js_scripts` directory.

### Browser Discovery (`osn_selenium.browsers_handler`)
*   `get_installed_browsers()`: Returns a list of installed browsers on Windows.
*   `get_version_of_browser(...)`: Gets the version of a specific browser.
*   `get_path_to_browser(...)`: Gets the installation path of a specific browser.

### Executors (`osn_selenium.executors`)
*   Provides synchronous (`sync`) and asynchronous (`trio_threads`) executors for JavaScript and CDP commands.
    *   `javascript.JSExecutor`: Executes predefined and custom JS scripts.
    *   `cdp.CDPExecutor`: Executes Chrome DevTools Protocol commands.

### WebDriver Implementations (`osn_selenium.webdrivers`)
*   Contains both synchronous (`sync`) and asynchronous (`trio_threads`) WebDriver classes.
    *   `chrome.ChromeWebDriver`: WebDriver for Google Chrome.
    *   `edge.EdgeWebDriver`: WebDriver for Microsoft Edge.
    *   `yandex.YandexWebDriver`: WebDriver for Yandex Browser.

### DevTools Module (`osn_selenium.dev_tools`)
*   A powerful system for interacting with the Chrome DevTools Protocol.
*   `manager.DevTools`: The main context manager for handling DevTools sessions.
*   `manager.DevToolsSettings`: Configuration for the DevTools manager.
*   `target.DevToolsTarget`: Represents and manages a single CDP target (e.g., a tab).
*   `domains.DomainsSettings`: Top-level settings for all CDP domains.
    *   `fetch.FetchSettings`: Configuration for intercepting network requests via the Fetch domain.
*   `logger`: A dedicated logging system for DevTools events.
    *   `LoggerSettings`, `LogEntry`, `TargetLogger`, `MainLogger`.

### Flags Management (`osn_selenium.flags`)
*   A structured system for managing browser startup flags.
*   `base.BrowserFlagsManager`: The core manager for arguments, attributes, and experimental options.
*   `blink.BlinkFlagsManager`: Extends the base manager with support for Blink-specific features.
*   `chrome.ChromeFlagsManager`, `edge.EdgeFlagsManager`, `yandex.YandexFlagsManager`: Specialized managers for each browser.

### Instance Wrappers (`osn_selenium.instances`)
*   Provides synchronous (`sync`) and asynchronous (`trio_threads`) wrappers around core Selenium objects to expose a unified API.
    *   `action_chains`: `ActionChains` and `HumanLikeActionChains`.
    *   `web_element`: `WebElement`.
    *   `alert`: `Alert`.
    *   And others for `Browser`, `BrowsingContext`, `Network`, `Storage`, etc.

## Future Notes

*   Add support for additional browsers like Firefox.
*   Expand built-in support for more CDP domains (e.g., Network, Page, Emulation).
*   Extend browser discovery utilities to support Linux and macOS.
*   Add more presets and complex behaviors to `HumanLikeActionChains`.