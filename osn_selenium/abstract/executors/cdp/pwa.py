from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractPwaCDPExecutor"]


class AbstractPwaCDPExecutor(ABC):
	@abstractmethod
	def change_app_user_settings(
			self,
			manifest_id: str,
			link_capturing: Optional[bool] = None,
			display_mode: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def get_os_app_state(self, manifest_id: str) -> Tuple[int, List[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def install(self, manifest_id: str, install_url_or_bundle_url: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def launch(self, manifest_id: str, url: Optional[str] = None) -> str:
		...
	
	@abstractmethod
	def launch_files_in_app(self, manifest_id: str, files: List[str]) -> List[str]:
		...
	
	@abstractmethod
	def open_current_page_in_app(self, manifest_id: str) -> None:
		...
	
	@abstractmethod
	def uninstall(self, manifest_id: str) -> None:
		...
