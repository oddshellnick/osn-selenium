from typing import List

import trio
from selenium.webdriver.common.bidi.cdp import (
    BrowserError,
    open_cdp
)

from osn_selenium.dev_tools.decorators import background_task_decorator
from osn_selenium.dev_tools.errors import cdp_end_exceptions
from osn_selenium.dev_tools.logger.target import build_target_logger
from osn_selenium.dev_tools.target.detach import DetachMixin
from osn_selenium.dev_tools.target.discovery import DiscoveryMixin
from osn_selenium.dev_tools.target.events import EventHandlersMixin
from osn_selenium.dev_tools._functions import (
    execute_cdp_command,
    wait_one
)


class LifecycleMixin(DiscoveryMixin, EventHandlersMixin, DetachMixin):
    """
    Mixin managing the main lifecycle of the DevTools target (setup, run, close).
    """

    async def run(self):
        """
        Starts the main lifecycle loop of the target.

        Initializes logging, establishes the CDP session, sets up event handling,
        runs background tasks, and waits for exit signals.

        Raises:
            BaseException: Handles and logs various exceptions during the lifecycle.
        """
        try:
            self._logger_send_channel, self._logger = build_target_logger(
                self.target_data, self._nursery_object, self._logger_settings
            )

            if self._target_type_log_accepted:
                await self._logger.run()

            await self.log_step(message=f"Target '{self.target_id}' added.")

            async with open_cdp(self.websocket_url) as new_connection:
                target_id_instance = self.devtools_package.get("target.TargetID").from_json(self.target_id)

                async with new_connection.open_session(target_id_instance) as new_session:
                    self._cdp_session = new_session

                    await self._setup_target()

                    if self._target_background_task is not None:
                        self._nursery_object.start_soon(
                            background_task_decorator(self._target_background_task), self
                        )

                    await wait_one(self.exit_event, self.about_to_stop_event)
        except* (BrowserError, RuntimeError):
            self.about_to_stop_event.set()
        except* cdp_end_exceptions:
            self.about_to_stop_event.set()
        except* BaseException as error:
            self.about_to_stop_event.set()
            await self.log_error(error=error)
        finally:
            await self._close_instances()
            await self._remove_target_func(self)

            self.stopped_event.set()

    async def _setup_target(self):
        """
        Configures the target session by enabling domains and starting listeners.

        Enables configured CDP domains, starts event listeners for them,
        and initializes target discovery and detach monitoring.

        Raises:
            cdp_end_exceptions: If connection issues occur.
            BaseException: If setup fails.
        """
        try:
            await self.log_step(message="Target setup started.")

            await self._setup_new_targets_attaching()

            target_ready_events: List[trio.Event] = []

            new_targets_listener_ready_event = trio.Event()
            target_ready_events.append(new_targets_listener_ready_event)

            self._nursery_object.start_soon(self._run_new_targets_listener, new_targets_listener_ready_event)
            self._nursery_object.start_soon(self._run_detach_checking,)

            for domain_name, domain_config in self._domains.model_dump(exclude_none=True).items():
                if domain_config.get("enable_func_path", None) is not None:
                    enable_func_kwargs = domain_config.get("enable_func_kwargs", {})

                    if (
                            domain_config["include_target_types"]
                            and self.type_ in domain_config["include_target_types"]
                            or domain_config["exclude_target_types"]
                            and self.type_ not in domain_config["exclude_target_types"]
                    ):
                        await execute_cdp_command(
                                self=self,
                                error_mode="log",
                                function=self.devtools_package.get(domain_config["enable_func_path"]),
                                **enable_func_kwargs
                        )

                domain_handlers_ready_event = trio.Event()
                target_ready_events.append(domain_handlers_ready_event)
                self._nursery_object.start_soon(
                        self._run_events_handlers,
                        domain_handlers_ready_event,
                        getattr(self._domains, domain_name)
                )

            for domain_handlers_ready_event in target_ready_events:
                await domain_handlers_ready_event.wait()

            await execute_cdp_command(
                    self=self,
                    error_mode="log",
                    function=self.devtools_package.get("runtime.run_if_waiting_for_debugger"),
            )

            await self.log_step(message="Target setup complete.")
        except* cdp_end_exceptions as error:
            raise error
        except* BaseException as error:
            await self.log_error(error=error)
            raise error

    async def _close_instances(self):
        """
        Closes all active resources, channels, and loggers associated with the target.
        """
        if self._new_target_receive_channel is not None:
            await self._new_target_receive_channel[0].aclose()
            await self._new_target_receive_channel[1].wait()
            self._new_target_receive_channel = None

        if self._detached_receive_channel is not None:
            await self._detached_receive_channel.aclose()
            self._detached_receive_channel = None

        if self._logger_send_channel is not None:
            await self._logger_send_channel.aclose()
            self._logger_send_channel = None

        if self._logger is not None:
            await self._logger.close()
            self._logger = None

        for channel in self._events_receive_channels.values():
            await channel[0].aclose()
            await channel[1].wait()

        self._events_receive_channels = {}

        if self.background_task_ended is not None:
            await self.background_task_ended.wait()
            self.background_task_ended = None
