from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


__all__ = ["AbstractCDPExecutor"]

if TYPE_CHECKING:
	from osn_selenium_cdp_v140.executors.abstract import AbstractCDP140Executor
	from osn_selenium_cdp_v141.executors.abstract import AbstractCDP141Executor
	from osn_selenium_cdp_v142.executors.abstract import AbstractCDP142Executor
	from osn_selenium_cdp_v143.executors.abstract import AbstractCDP143Executor
	from osn_selenium_cdp_v144.executors.abstract import AbstractCDP144Executor


class AbstractCDPExecutor(ABC):
	"""
	Global abstract interface for accessing different versions of CDP.
	"""

	@property
	@abstractmethod
	def v140(self) -> "AbstractCDP140Executor":
		"""
		Access CDP version 140 interface.
		"""

		...

	@property
	@abstractmethod
	def v141(self) -> "AbstractCDP141Executor":
		"""
		Access CDP version 141 interface.
		"""

		...

	@property
	@abstractmethod
	def v142(self) -> "AbstractCDP142Executor":
		"""
		Access CDP version 142 interface.
		"""

		...

	@property
	@abstractmethod
	def v143(self) -> "AbstractCDP143Executor":
		"""
		Access CDP version 143 interface.
		"""

		...

	@property
	@abstractmethod
	def v144(self) -> "AbstractCDP144Executor":
		"""
		Access CDP version 144 interface.
		"""

		...
