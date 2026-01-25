import trio
from selenium.webdriver.common.alert import Alert as legacyAlert
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile
)
from osn_selenium.exceptions.protocol import (
	ProtocolComplianceError
)
from typing import (
	Any,
	Optional,
	Type,
	TypeVar,
	Union,
	overload
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
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
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
from osn_selenium.instances.protocols import (
	SyncInstanceWrapper,
	TrioThreadInstanceWrapper
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext
)
from osn_selenium.instances._typehints import (
	ACTION_CHAINS_TYPEHINT,
	ALERT_TYPEHINT,
	ANY_ABSTRACT_INSTANCE_TYPEHINT,
	ANY_LEGACY_INSTANCE_TYPEHINT,
	BROWSER_TYPEHINT,
	BROWSING_CONTEXT_TYPEHINT,
	DIALOG_TYPEHINT,
	FEDCM_TYPEHINT,
	MOBILE_TYPEHINT,
	NETWORK_TYPEHINT,
	PERMISSIONS_TYPEHINT,
	SCRIPT_TYPEHINT,
	SHADOW_ROOT_TYPEHINT,
	STORAGE_TYPEHINT,
	SWITCH_TO_TYPEHINT,
	WEB_DRIVER_WAIT_TYPEHINT,
	WEB_ELEMENT_TYPEHINT,
	WEB_EXTENSION_TYPEHINT
)


__all__ = [
	"get_legacy_frame_reference",
	"get_legacy_instance",
	"get_sync_instance_wrapper",
	"get_trio_thread_instance_wrapper"
]

_SYNC_WRAPPER_TYPE = TypeVar("_SYNC_WRAPPER_TYPE", bound=SyncInstanceWrapper)
_TRIO_THREAD_WRAPPER_TYPE = TypeVar("_TRIO_THREAD_WRAPPER_TYPE", bound=TrioThreadInstanceWrapper)


@overload
def get_legacy_instance(instance: None) -> None:
	...


@overload
def get_legacy_instance(instance: Optional[ALERT_TYPEHINT]) -> Optional[legacyAlert]:
	...


@overload
def get_legacy_instance(instance: Optional[FEDCM_TYPEHINT]) -> Optional[legacyFedCM]:
	...


@overload
def get_legacy_instance(instance: Optional[DIALOG_TYPEHINT]) -> Optional[legacyDialog]:
	...


@overload
def get_legacy_instance(instance: Optional[MOBILE_TYPEHINT]) -> Optional[legacyMobile]:
	...


@overload
def get_legacy_instance(instance: Optional[SCRIPT_TYPEHINT]) -> Optional[legacyScript]:
	...


@overload
def get_legacy_instance(instance: Optional[BROWSER_TYPEHINT]) -> Optional[legacyBrowser]:
	...


@overload
def get_legacy_instance(instance: Optional[NETWORK_TYPEHINT]) -> Optional[legacyNetwork]:
	...


@overload
def get_legacy_instance(instance: Optional[STORAGE_TYPEHINT]) -> Optional[legacyStorage]:
	...


@overload
def get_legacy_instance(instance: Optional[SWITCH_TO_TYPEHINT]) -> Optional[legacySwitchTo]:
	...


@overload
def get_legacy_instance(instance: Optional[SHADOW_ROOT_TYPEHINT]) -> Optional[legacyShadowRoot]:
	...


@overload
def get_legacy_instance(instance: Optional[WEB_ELEMENT_TYPEHINT]) -> Optional[legacyWebElement]:
	...


@overload
def get_legacy_instance(instance: Optional[PERMISSIONS_TYPEHINT]) -> Optional[legacyPermissions]:
	...


@overload
def get_legacy_instance(instance: Optional[ACTION_CHAINS_TYPEHINT]) -> Optional[legacyActionChains]:
	...


@overload
def get_legacy_instance(instance: Optional[WEB_EXTENSION_TYPEHINT]) -> Optional[legacyWebExtension]:
	...


@overload
def get_legacy_instance(instance: Optional[WEB_DRIVER_WAIT_TYPEHINT]) -> Optional[legacyWebDriverWait]:
	...


@overload
def get_legacy_instance(instance: Optional[BROWSING_CONTEXT_TYPEHINT]) -> Optional[legacyBrowsingContext]:
	...


def get_legacy_instance(
		instance: Optional[Union[ANY_ABSTRACT_INSTANCE_TYPEHINT, ANY_LEGACY_INSTANCE_TYPEHINT]]
) -> Optional[ANY_LEGACY_INSTANCE_TYPEHINT]:
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
		ExpectedTypeError: If the input instance is of an unsupported type.
	"""
	
	if instance is None:
		return None
	
	if isinstance(instance, ANY_ABSTRACT_INSTANCE_TYPEHINT):
		return instance.legacy
	
	if isinstance(instance, ANY_LEGACY_INSTANCE_TYPEHINT):
		return instance
	
	raise NotExpectedTypeError(
			expected_type=(ANY_ABSTRACT_INSTANCE_TYPEHINT, ANY_LEGACY_INSTANCE_TYPEHINT, None),
			received_instance=instance
	)


def get_trio_thread_instance_wrapper(
		wrapper_class: Type[_TRIO_THREAD_WRAPPER_TYPE],
		legacy_object: Any,
		lock: trio.Lock,
		limiter: trio.CapacityLimiter,
) -> _TRIO_THREAD_WRAPPER_TYPE:
	"""
	Creates a Trio-compatible thread instance wrapper for a legacy Selenium object.

	Args:
		wrapper_class (Type[_TRIO_THREAD_WRAPPER_TYPE]): The class used to wrap the legacy object.
		legacy_object (Any): The legacy Selenium object to be wrapped.
		lock (trio.Lock): The lock for Trio synchronization.
		limiter (trio.CapacityLimiter): The capacity limiter for Trio.

	Returns:
		_TRIO_THREAD_WRAPPER_TYPE: An instance of the wrapper class.

	Raises:
		TypeIsNotWrapper: If the provided wrapper_class does not implement TrioThreadInstanceWrapper.
	"""
	
	if not isinstance(wrapper_class, TrioThreadInstanceWrapper):
		raise ProtocolComplianceError(instance=wrapper_class, expected_protocols=TrioThreadInstanceWrapper)
	
	return wrapper_class.from_legacy(legacy_object=legacy_object, lock=lock, limiter=limiter)


def get_sync_instance_wrapper(wrapper_class: Type[_SYNC_WRAPPER_TYPE], legacy_object: Any) -> _SYNC_WRAPPER_TYPE:
	"""
	Creates a synchronous instance wrapper for a legacy Selenium object.

	Args:
		wrapper_class (Type[_SYNC_WRAPPER_TYPE]): The class used to wrap the legacy object.
		legacy_object (Any): The legacy Selenium object to be wrapped.

	Returns:
		_SYNC_WRAPPER_TYPE: An instance of the wrapper class.

	Raises:
		TypeIsNotWrapper: If the provided wrapper_class does not implement SyncInstanceWrapper.
	"""
	
	if not isinstance(wrapper_class, SyncInstanceWrapper):
		raise ProtocolComplianceError(instance=wrapper_class, expected_protocols=SyncInstanceWrapper)
	
	return wrapper_class.from_legacy(legacy_object=legacy_object)


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
	
	return get_legacy_instance(instance=frame_reference)
