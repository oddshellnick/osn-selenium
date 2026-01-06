from typing import (
	Any,
	Callable,
	Dict,
	ParamSpec,
	TypeVar
)
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.executors.sync.cdp.target import TargetCDPExecutor


class CDPExecutor(AbstractCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
		
		self._target = TargetCDPExecutor(execute_function=self._prepare_and_execute)
	
	def execute(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return self._execute_function(cmd, cmd_args)
	
	def _prepare_and_execute(self, command_name: str, locals_: Dict[str, Any]) -> Any:
		locals_.pop("self")
		return self.execute(cmd=command_name, cmd_args=locals_)
	
	@property
	def target(self) -> TargetCDPExecutor:
		return self._target
