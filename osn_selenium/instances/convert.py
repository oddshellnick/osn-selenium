from typing import Any, Optional, Union
from selenium.webdriver.remote.webelement import WebElement
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from osn_selenium.instances.types import (
	ACTION_CHAINS_TYPEHINT,
	ALERT_TYPEHINT,
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
	WEB_ELEMENT_TYPEHINT,
	WEB_EXTENSION_TYPEHINT
)


def get_legacy_instance(instance: Optional[Any]) -> Optional[Any]:
	if instance is None:
		return None
	
	if isinstance(
			instance,
			(
					WEB_ELEMENT_TYPEHINT,
					ACTION_CHAINS_TYPEHINT,
					ALERT_TYPEHINT,
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
					WEB_EXTENSION_TYPEHINT,
			)
	):
		return instance.legacy
	
	return instance


def get_legacy_web_element(element: Optional[WEB_ELEMENT_TYPEHINT]) -> Optional[WebElement]:
	if element is None:
		return None
	
	if isinstance(element, AbstractWebElement):
		return element.legacy
	elif isinstance(element, WebElement):
		return element
	
	raise ValueError(f"Invalid WebElement type {type(element)}")


def get_legacy_frame_reference(frame_reference: Union[str, int, Optional[WEB_ELEMENT_TYPEHINT]]) -> Union[str, int, Optional[WebElement]]:
	if isinstance(frame_reference, (str, int)):
		return frame_reference
	
	return get_legacy_web_element(frame_reference)
