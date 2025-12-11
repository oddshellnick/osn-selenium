from typing import TYPE_CHECKING, Union
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.alert import Alert as legacyAlert
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile
)
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser
)
from selenium.webdriver.common.bidi.network import (
	Network as legacyNetwork
)
from selenium.webdriver.common.bidi.storage import (
	Storage as legacyStorage
)
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)
from selenium.webdriver.common.bidi.permissions import (
	Permissions as legacyPermissions
)
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext
)


if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains
	from osn_selenium.abstract.instances.alert import AbstractAlert
	from osn_selenium.abstract.instances.browser import AbstractBrowser
	from osn_selenium.abstract.instances.browsing_context import AbstractBrowsingContext
	from osn_selenium.abstract.instances.dialog import AbstractDialog
	from osn_selenium.abstract.instances.fedcm import AbstractFedCM
	from osn_selenium.abstract.instances.mobile import AbstractMobile
	from osn_selenium.abstract.instances.network import AbstractNetwork
	from osn_selenium.abstract.instances.permissions import AbstractPermissions
	from osn_selenium.abstract.instances.script import AbstractScript
	from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
	from osn_selenium.abstract.instances.storage import AbstractStorage
	from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
	from osn_selenium.abstract.instances.web_element import AbstractWebElement
	from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
	
	from osn_selenium.instances.sync.web_element import WebElement as SyncWebElement


WEB_ELEMENT_TYPEHINT = Union["AbstractWebElement", WebElement]
ACTION_CHAINS_TYPEHINT = Union["AbstractActionChains", legacyActionChains]
ALERT_TYPEHINT = Union["AbstractAlert", legacyAlert]
BROWSER_TYPEHINT = Union["AbstractBrowser", legacyBrowser]
BROWSING_CONTEXT_TYPEHINT = Union["AbstractBrowsingContext", legacyBrowsingContext]
DIALOG_TYPEHINT = Union["AbstractDialog", legacyDialog]
FEDCM_TYPEHINT = Union["AbstractFedCM", legacyFedCM]
MOBILE_TYPEHINT = Union["AbstractMobile", legacyMobile]
NETWORK_TYPEHINT = Union["AbstractNetwork", legacyNetwork]
PERMISSIONS_TYPEHINT = Union["AbstractPermissions", legacyPermissions]
SCRIPT_TYPEHINT = Union["AbstractScript", legacyScript]
SHADOW_ROOT_TYPEHINT = Union["AbstractShadowRoot", legacyShadowRoot]
STORAGE_TYPEHINT = Union["AbstractStorage", legacyStorage]
SWITCH_TO_TYPEHINT = Union["AbstractSwitchTo", legacySwitchTo]
WEB_EXTENSION_TYPEHINT = Union["AbstractWebExtension", legacyWebExtension]
