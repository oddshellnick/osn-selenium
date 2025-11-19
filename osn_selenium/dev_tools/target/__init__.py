from osn_selenium.dev_tools.target.lifecycle import LifecycleMixin


__all__ = ["DevToolsTarget"]


class DevToolsTarget(LifecycleMixin):
	"""
	Manages the DevTools Protocol session and event handling for a specific browser target.

	Each `DevToolsTarget` instance represents a single CDP target (e.g., a browser tab,
	an iframe, or a service worker) and handles its dedicated CDP session, event listeners,
	and associated logging.
	"""
	
	pass
