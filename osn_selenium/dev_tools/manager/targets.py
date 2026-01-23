from typing import Any, List, Optional
from osn_selenium.dev_tools.models import TargetData
from osn_selenium.dev_tools.target import DevToolsTarget
from osn_selenium.dev_tools.manager.logging import LoggingMixin
from osn_selenium.dev_tools._exception_helpers import log_exception
from osn_selenium.dev_tools.logger.models import CDPTargetTypeStats
from osn_selenium.exceptions.devtools import (
	BidiConnectionNotEstablishedError,
	CDPEndExceptions
)


__all__ = ["TargetsMixin"]


class TargetsMixin(LoggingMixin):
	"""
	Mixin for adding, removing, and retrieving DevTools targets.
	"""
	
	async def _remove_target(self, target: DevToolsTarget) -> Optional[bool]:
		"""
		Removes a target ID from the List of currently handled targets.

		This method also triggers the removal of the target's specific logger channel
		and updates overall logging statistics.

		Args:
			target (DevToolsTarget): The target instance to remove.

		Returns:
			Optional[bool]: True if the target ID was successfully removed, False if it was not found.
							Returns None if an exception occurs.
		"""
		
		try:
			async with self.targets_lock:
				if target.target_id in self._handling_targets:
					self._cdp_targets_types_stats[target.type_].num_targets -= 1
		
					target = self._handling_targets.pop(target.target_id)
					await target.log_cdp_step(message=f"Target '{target.target_id}' removed.")
					await target.stop()
		
					await self._add_main_cdp_log()
		
					return True
				else:
					return False
		except CDPEndExceptions:
			pass
		except BaseException as error:
			log_exception(error)
	
	async def _add_target(self, target_event: Any, is_main_target: bool = False) -> Optional[bool]:
		"""
		Adds a new browser target to the manager based on a target event.

		This method processes events like `TargetCreated` or `AttachedToTarget`
		to initialize and manage new `DevToolsTarget` instances. It ensures
		that targets are not added if the manager is closing or if they already exist.

		Args:
			target_event (Any): The event object containing target information.
								 Expected to have a `target_info` attribute or be the target info itself.

		Returns:
			Optional[bool]: True if a new target was successfully added and started,
							False if the target already existed or was filtered,
							or None if an error occurred.

		Raises:
			BaseException: Catches and logs any unexpected errors during target addition.
		"""
		
		try:
			if hasattr(target_event, "target_info"):
				target_info = target_event.target_info
			else:
				target_info = target_event
		
			async with self.targets_lock:
				target_id = target_info.target_id
		
				if self._is_closing:
					return False
		
				if target_id not in self._handling_targets:
					self._handling_targets[target_id] = DevToolsTarget(
							target_data=TargetData(
									target_id=target_id,
									type_=target_info.type_,
									title=target_info.title,
									url=target_info.url,
									attached=target_info.attached,
									can_access_opener=target_info.can_access_opener,
									opener_id=target_info.opener_id,
									opener_frame_id=target_info.opener_frame_id,
									browser_context_id=target_info.browser_context_id,
									subtype=target_info.subtype,
							),
							is_main_target=is_main_target,
							logger_settings=self._logger_settings,
							domains_settings=self._domains_settings,
							devtools_package=self._devtools_package,
							websocket_url=self._websocket_url,
							new_targets_filter_list=self._new_targets_filter,
							new_targets_buffer_size=self._new_targets_buffer_size,
							nursery=self._nursery_object,
							exit_event=self.exit_event,
							fingerprint_injection_script=self._fingerprint_injection_script,
							target_background_task=self._target_background_task,
							add_target_func=self._add_target,
							remove_target_func=self._remove_target,
							add_cdp_log_func=self._add_cdp_log,
							add_fingerprint_log_func=self._add_fingerprint_log,
					)
		
					if target_info.type_ not in self._cdp_targets_types_stats:
						self._cdp_targets_types_stats[target_info.type_] = CDPTargetTypeStats(num_targets=1)
					else:
						self._cdp_targets_types_stats[target_info.type_].num_targets += 1
		
					await self._add_main_cdp_log()
		
					self._nursery_object.start_soon(self._handling_targets[target_id].run)
		
					return True
				else:
					self._handling_targets[target_id].type_ = target_info.type_
					self._handling_targets[target_id].title = target_info.title
					self._handling_targets[target_id].url = target_info.url
					self._handling_targets[target_id].attached = target_info.attached
					self._handling_targets[target_id].can_access_opener = target_info.can_access_opener
					self._handling_targets[target_id].opener_id = target_info.opener_id
					self._handling_targets[target_id].opener_frame_id = target_info.opener_frame_id
					self._handling_targets[target_id].browser_context_id = target_info.browser_context_id
					self._handling_targets[target_id].subtype = target_info.subtype
		
					return False
		except* CDPEndExceptions:
			pass
		except* BaseException as error:
			log_exception(error)
			raise error
	
	async def _get_all_targets(self) -> List[Any]:
		"""
		Retrieves a List of all currently active browser targets.

		Returns:
			List[Any]: A List of target objects, each containing information like target ID, type, and URL.

		Raises:
			BidiConnectionNotEstablishedError: If the BiDi connection is not active.
		"""
		
		try:
			if self._bidi_connection_object is not None:
				targets_filter = self._devtools_package.get("target.TargetFilter")(
						[
							{"exclude": False, "type": "page"},
							{"exclude": False, "type": "tab"},
							{"exclude": True}
						]
				)
		
				return await self._bidi_connection_object.session.execute(self._devtools_package.get("target.get_targets")(targets_filter))
		
			raise BidiConnectionNotEstablishedError()
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
