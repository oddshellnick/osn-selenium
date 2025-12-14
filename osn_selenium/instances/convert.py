from typing import (
	Optional,
	Union,
	overload
)
from osn_selenium.abstract.instances.alert import AbstractAlert
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from selenium.webdriver.common.alert import Alert as legacyAlert
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.abstract.instances.dialog import AbstractDialog
from osn_selenium.abstract.instances.mobile import AbstractMobile
from osn_selenium.abstract.instances.script import AbstractScript
from osn_selenium.abstract.instances.browser import AbstractBrowser
from osn_selenium.abstract.instances.network import AbstractNetwork
from osn_selenium.abstract.instances.storage import AbstractStorage
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile
)
from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)
from osn_selenium.abstract.instances.action_chains import AbstractActionChains
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
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
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)
from osn_selenium.abstract.instances.browsing_context import (
	AbstractBrowsingContext
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
from osn_selenium.instances.types import (
	ANY_ABSTRACT_TYPE,
	ANY_LEGACY_TYPE,
	WEB_ELEMENT_TYPEHINT
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext
)


@overload
def get_legacy_instance(instance: Optional[AbstractAlert]) -> Optional[legacyAlert]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractFedCM]) -> Optional[legacyFedCM]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractDialog]) -> Optional[legacyDialog]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractMobile]) -> Optional[legacyMobile]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractScript]) -> Optional[legacyScript]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractBrowser]) -> Optional[legacyBrowser]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractNetwork]) -> Optional[legacyNetwork]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractStorage]) -> Optional[legacyStorage]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractSwitchTo]) -> Optional[legacySwitchTo]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractShadowRoot]) -> Optional[legacyShadowRoot]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractWebElement]) -> Optional[legacyWebElement]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractPermissions]) -> Optional[legacyPermissions]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractActionChains]) -> Optional[legacyActionChains]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractWebExtension]) -> Optional[legacyWebExtension]:
	...


@overload
def get_legacy_instance(instance: Optional[AbstractBrowsingContext]) -> Optional[legacyBrowsingContext]:
	...


@overload
def get_legacy_instance(instance: None) -> None:
	...


def get_legacy_instance(instance: Optional[Union[ANY_ABSTRACT_TYPE, ANY_LEGACY_TYPE]]) -> Optional[ANY_LEGACY_TYPE]:
	"""
	Converts an abstract Selenium instance to its corresponding legacy Selenium instance.

	This function handles various types of Selenium objects, including browser contexts,
	web elements, alerts, and more. It returns the legacy object if the input is an
	abstract instance, or the input itself if it's already a legacy instance or None.

	Args:
		instance (Optional[Union[ANY_ABSTRACT_TYPE, ANY_LEGACY_TYPE]]): The instance to convert.
																	   Can be an abstract instance,
																	   a legacy instance, or None.

	Returns:
		Optional[ANY_LEGACY_TYPE]: The converted legacy instance,
															 or None if the input was None.

	Raises:
		ValueError: If the input instance is of an unsupported type.
	"""
	
	if instance is None:
		return None
	
	if isinstance(instance, ANY_ABSTRACT_TYPE):
		return instance.legacy
	
	if isinstance(instance, ANY_LEGACY_TYPE):
		return instance
	
	raise ValueError(
			f"Invalid instance type {type(instance)}. Valid types are " f"{ANY_ABSTRACT_TYPE} and {ANY_LEGACY_TYPE} or None."
	)


def get_legacy_frame_reference(frame_reference: Optional[Union[str, int, WEB_ELEMENT_TYPEHINT]]) -> Optional[Union[str, int, legacyWebElement]]:
	"""
	Converts a frame reference to its legacy Selenium equivalent.

	The frame reference can be a string (frame name), an integer (frame index),
	an AbstractWebElement, or a legacy WebElement. If it's a web element,
	it is converted to its legacy WebElement form using `get_legacy_instance`.

	Args:
		frame_reference (Optional[Union[str, int, WEB_ELEMENT_TYPEHINT]]): The reference to the frame.

	Returns:
		Optional[Union[str, int, legacyWebElement]]: The legacy frame reference,
													which can be a string, integer,
													or a legacy WebElement, or None.
	"""
	
	if isinstance(frame_reference, (str, int)):
		return frame_reference
	
	return get_legacy_instance(frame_reference)
