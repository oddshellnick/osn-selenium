from osn_selenium.dev_tools.manager.settings import SettingsMixin
from osn_selenium.dev_tools.manager.lifecycle import LifecycleMixin


__all__ = ["DevTools"]


class DevTools(LifecycleMixin, SettingsMixin):
	"""
	Main entry point for managing Chrome DevTools Protocol (CDP) interactions.

	This class combines lifecycle management, settings configuration, and target handling
	to provide a comprehensive interface for controlling browser behavior via CDP.
	"""
	
	pass
