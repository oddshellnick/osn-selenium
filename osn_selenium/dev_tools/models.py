from typing import Optional
from osn_selenium._base_models import DictModel


__all__ = ["FingerprintData", "TargetData"]


class TargetData(DictModel):
	"""
	Dataclass to hold essential information about a browser target.

	Attributes:
		target_id (Optional[str]): The unique identifier for the target.
		type_ (Optional[str]): The type of the target (e.g., "page", "iframe", "worker").
		title (Optional[str]): The title of the target (e.g., the page title).
		url (Optional[str]): The URL of the target.
		attached (Optional[bool]): Indicates if the DevTools session is currently attached to this target.
		can_access_opener (Optional[bool]): Whether the target can access its opener.
		opener_id (Optional[str]): The ID of the opener target.
		opener_frame_id (Optional[str]): The ID of the opener frame.
		browser_context_id (Optional[str]): The browser context ID associated with the target.
		subtype (Optional[str]): Subtype of the target.
	"""
	
	target_id: Optional[str] = None
	type_: Optional[str] = None
	title: Optional[str] = None
	url: Optional[str] = None
	attached: Optional[bool] = None
	can_access_opener: Optional[bool] = None
	opener_id: Optional[str] = None
	opener_frame_id: Optional[str] = None
	browser_context_id: Optional[str] = None
	subtype: Optional[str] = None


class FingerprintData(DictModel):
	"""
	Dataclass representing detected fingerprinting activity.

	Attributes:
		api (str): The API that was accessed.
		used_method (str): The method called.
		stacktrace (Optional[str]): The stack trace where the access occurred.
	"""
	
	api: str
	used_method: str
	stacktrace: Optional[str]
