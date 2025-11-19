from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractBrowserCDPExecutor"]


class AbstractBrowserCDPExecutor(ABC):
	@abstractmethod
	def add_privacy_sandbox_coordinator_key_config(
			self,
			api: str,
			coordinator_origin: str,
			key_config: str,
			browser_context_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def add_privacy_sandbox_enrollment_override(self, url: str) -> None:
		...
	
	@abstractmethod
	def cancel_download(self, guid: str, browser_context_id: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def close(self) -> None:
		...
	
	@abstractmethod
	def crash(self) -> None:
		...
	
	@abstractmethod
	def crash_gpu_process(self) -> None:
		...
	
	@abstractmethod
	def execute_browser_command(self, command_id: str) -> None:
		...
	
	@abstractmethod
	def get_browser_command_line(self) -> List[str]:
		...
	
	@abstractmethod
	def get_histogram(self, name: str, delta: Optional[bool] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_histograms(self, query: Optional[str] = None, delta: Optional[bool] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_version(self) -> Tuple[str, str, str, str, str]:
		...
	
	@abstractmethod
	def get_window_bounds(self, window_id: int) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_window_for_target(self, target_id: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
		...
	
	@abstractmethod
	def grant_permissions(
			self,
			permissions: List[str],
			origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def reset_permissions(self, browser_context_id: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_contents_size(
			self,
			window_id: int,
			width: Optional[int] = None,
			height: Optional[int] = None
	) -> None:
		...
	
	@abstractmethod
	def set_dock_tile(self, badge_label: Optional[str] = None, image: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_download_behavior(
			self,
			behavior: str,
			browser_context_id: Optional[str] = None,
			download_path: Optional[str] = None,
			events_enabled: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def set_permission(
			self,
			permission: Dict[str, Any],
			setting: str,
			origin: Optional[str] = None,
			embedded_origin: Optional[str] = None,
			browser_context_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def set_window_bounds(self, window_id: int, bounds: Dict[str, Any]) -> None:
		...
