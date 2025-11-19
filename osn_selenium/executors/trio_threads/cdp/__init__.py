from typing import Any, Awaitable, Callable, Dict, ParamSpec, TypeVar

from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.executors.trio_threads.cdp.target import TargetCDPExecutor


FUNCTION_INPUT = ParamSpec("FUNCTION_INPUT")
FUNCTION_OUTPUT = TypeVar("FUNCTION_OUTPUT")
EXECUTE_FUNCTION = Callable[FUNCTION_INPUT, Awaitable[FUNCTION_OUTPUT]]


class CDPExecutor(AbstractCDPExecutor):
    def __init__(self, execute_function: EXECUTE_FUNCTION):
        self._execute_function = execute_function
        self._target = TargetCDPExecutor(execute_function=self._prepare_and_execute)

    @property
    def target(self) -> TargetCDPExecutor:
        return self._target

    async def execute(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
        return self._execute_function(cmd, cmd_args)

    async def _prepare_and_execute(self, command_name: str, locals_: Dict[str, Any]) -> Any:
        locals_.pop("self")
        return self.execute(cmd=command_name, cmd_args=locals_)
